#
# This Dockerfile creates a .NET Fuzzing environment using afl + SharpFuzz on focal.
#
# On Linux Host you may run ./prefuzz.sh before starting the container
#
# You may adjust the NHapi package in the two .csproj files
# Packages in the local folder are preffered over remote nuget first
#
# How to Run (cwd inside Docker dir)
#       $ docker build -t nhapifuzz:1.2 .
#       $ docker run -d nhapifuzz:1.2
#       
#       Container runs indefinetly until its stopped manually
#       Use $ docker ps   to get container name
#       Connect with
#           $ docker exec -it [container name] /bin/bash
#
#       Inside the Docker container you can
#           Edit amount of cores used and other paramters with $ vim Scripts/run.sh
#           Start Fuzzing runs with $ fuzz &
#               You can CTRL+D out of the container after and reconnect with docker exec -it [container name] /bin/bash to reset terminal
#               After starting a fuzzing run, use $ whatsup [fuzzing_out_dir] to get updating results screen
#               Copy the fuzzing results out of the container with docker cp when finished
#
#           Deduplicate and minimize fuzzing results with $ minFindings
#               First use docker cp to copy fuzzing results into the container       
#               Deduplicate and minimize inputs with $ minFindings
#                   Example: $ minFindings "Crashes/id*" OutDir 5.0 1 4


# Build from base image with dotnet sdk on Ubuntu focal
FROM mcr.microsoft.com/dotnet/sdk:3.1-focal AS nhapi-fuzz-env
LABEL maintainer="github.com/JlKmn"
WORKDIR /app

# Install needed/useful packages
RUN apt update && apt install -y gcc make wget vim ranger unzip locales

# Install AFL
RUN wget https://github.com/google/AFL/archive/refs/tags/v2.57b.tar.gz
RUN tar -xvf v2.57b.tar.gz
WORKDIR /app/AFL-2.57b
RUN make install

# Install SharpFuzz as dotnet tool
RUN dotnet tool install --global SharpFuzz.CommandLine

# Set Environment Variable to skip instrumentation check in AFL + add sharpfuzz to path
ENV PATH="${PATH}:/root/.dotnet/tools"
ENV AFL_SKIP_BIN_CHECK=true
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Copy Packages (needed .nupkg packages), Inputs, Scripts and Fuzzing Harness project files
COPY Inputs /app/Inputs/
COPY Scripts /app/Scripts
COPY Harness /app/Harness

# Copy NHapi.Fuzz project files and restore + publish
WORKDIR /app/Harness/nHapi.Fuzz
RUN dotnet publish

# Copy NHapi.Fuzz project files and restore + publish
WORKDIR /app/Harness/nHapi.RunOnce
RUN dotnet publish

# Reset Workdir to /app
WORKDIR /app

# Instrument the NHapi dll 
RUN sharpfuzz Harness/nHapi.Fuzz/bin/Debug/netcoreapp3.1/NHapi.Base.dll
RUN sharpfuzz Harness/nHapi.Fuzz/bin/Debug/netcoreapp3.1/NHapi.Model.V27.dll
RUN sharpfuzz Harness/nHapi.RunOnce/bin/Debug/netcoreapp3.1/NHapi.Base.dll
RUN sharpfuzz Harness/nHapi.RunOnce/bin/Debug/netcoreapp3.1/NHapi.Model.V27.dll

# Set script aliases
RUN echo 'alias minFindings="/app/Scripts/Minimizer/minFindings.py"' >> /root/.bashrc
RUN echo 'alias whatsup="/app/Scripts/whatsup.py"' >> /root/.bashrc
RUN echo 'alias fuzz="/app/Scripts/run.sh"' >> /root/.bashrc
RUN chmod +x /app/Scripts/Minimizer/minFindings.py /app/Scripts/whatsup.py /app/Scripts/run.sh

# Container runs indefinitely until its stopped
CMD tail -f /dev/null