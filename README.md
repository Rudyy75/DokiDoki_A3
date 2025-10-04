# DokiDoki_A3
Differences between Client-Service based interaction and Publisher-Subscriber based interaction:  


Publisher–Subscriber:  
The publisher keeps sending messages when told to (turtle at (x,y))  
Any subscribers tuned in will read them  
No one asks for it — info just keeps flowing  

Client–Service:  
The client asks for something specific (make turtle move in a circle)  
The service listens, does the job, and replies once (Done, moved the turtle in a circle)  
It’s a request–response, not continuous  

Pub-sub = ongoing stream of info  
Client-service = one-time request and reply
