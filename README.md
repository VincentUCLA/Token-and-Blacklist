# Redis-based token management and violator recording system
### Tech Stack
Python, Redis
### How to use
This project include 3 parts: 
1. Redis-based key-value timer record:
   1. Upon initialization, you can set the Redis DB, DB name, idle time and life time. 
   2. All key-value pair will expire if not extended within idle time, and after life time.
   3. Upon generation of key-value pair, it is allowed to include other information as JSON format in the parameter of _value_
2. Token management system based on 1
   1. The thing added to 1 is we record the clients' IP addresses and user-agent to identify it is unique.
3. Redis-based IP blacklist system.
   1. Upon initialization, you can set Redis DB, violation limit within a certain period, and block time.
   2. After the attacker exceeds the violation limit within a certain period, we block it for a certain time. 

The core functions were thoroughly tested by test scripts. The source code is very well-commented and serves as document. 

### Design
#### Real-world problem
Token can be hijacked from the client (sidejacking), or attacked by brute-force, causing Broken Authentication. (OWASP Top 10 #2)
#### Analysis
Token should be:
- meaningless, 
- specific to the client (identified by IP address and/or client certificate, for example)
- with idle timeout and absolute timeout (in our case, 2 min and 20 min). 

So that any violation can be detected and recorded. 
#### Design
- Use Redis hash set. Tokens as key and the details (timeouts, IP, etc.) as value. 
- Each time of access we extend the time limit by idle timeout if everything valid, otherwise we remove the token. 
- We identify wrong combination of token & client and using expired token as violation and record it to specific IP. 
- If some IP exceeds violation limit in a certain period, we block it temporarily. (in our case, 2 hrs)
