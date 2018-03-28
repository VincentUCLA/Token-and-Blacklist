# Redis-based token management and violator recording system
### Tech Stack
Python, Redis, Async
### Usage

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