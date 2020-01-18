# Linux_FileSystem_Silmulation
Emulate the filesystem of Linux 

In this project, I built a client/server based file system where the client accessed data blocks stored at a server. 


I extend my file system to multiple servers with support for redundant block storage. 


The project will expose the practical issues in the design of systems including: client/service, networking, and fault tolerance.
 
 
My goal in the project is to distribute and store data across multiple data servers to 1) reduce their load (i.e., distributing requests across servers holding replicas), provide increased aggregate capacity, and fault tolerance. 


My redundant block storage should follow the general approach described for RAID-5. I distribute data and parity information across servers, at the granularity of the block size from my configuration file. 

