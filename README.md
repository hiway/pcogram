# pcogram

Python: API + command-line client for pcogram.


## API

### /api/register

Register an account on pcogram.com.
```
$ curl https://pcogram.com/api/register \
  -X POST \
  -d '{"username":"","email":"","password":""}' 
```
##### Request:
```json
{
  "username":"batman",
  "email":"beacon@batmail.com",
  "password":"batsb4tsba7s2atsbat5",
}
```

- `username`:
  - may contain only these characters: A-Z, a-z, 0-9 and _ (underscore).
  - must be at leat 3 characters long.
  - can be at most 32 characters long.
- `email`:
  - must be a valid email.
  - can be at most 256 characters long.
  - if you use plus-address:
    - plus-address (`email+label@example.com`) is valid.
    - plus-addressed email may not be used to create another account, even if `+label` is different.
    - the `+label` part is required to reset password.
- `password`:
  - unicode
  - must be at least 8 characters long.
  - can be at most 256 characters long.
 
 ##### Response:
 
 ```json
{
  "message": "Welcome to pcogram!",
  "data":{
    "username":"batman",
    "email":"beacon@batmail.com"
  }
}
``` 


 ##### Errors:
 
 ```json
{
  "message": "Username 'twoface' is not available. Please try another username?",
  "error": 2000
}
```

- `2000` Username not available.  
- `2002` Username permitted-characters check failed.  
- `2003` Username length check failed.  
- `2010` Email failed validation.
- `2011` Email length check failed.
- `2012` Email already used or banned.  
- `2020` Password length check failed.
- `9900` Unexpected error. 
- `9901` Unexpected error, try later. 

 
### /api/login

```
$ curl https://pcogram.com/api/login \
  -X POST \
  -d '{"username":"","password":""}' 
```

##### Request:
```json
{
  "username":"batman",
  "password":"batsb4tsba7s2atsbat5",
}
```

- `username`:
  - may contain only these characters: A-Z, a-z, 0-9 and _ (underscore).
  - must be at leat 3 characters long.
  - can be at most 32 characters long.
- `password`:
  - unicode
  - must be at least 8 characters long.
  - can be at most 256 characters long.
 
 ##### Response:
 
 ```json
{
  "message": "Here we go!",
  "data":{
    "username":"batman",
    "token":"PCOGRAM-TOKEN"
  }
}
``` 

 ##### Errors:
 
 ```json
{
  "message": "Username 'bathman' not found or password is incorrect.",
  "error": 2100
}
```

- `2100` Invalid username or password.  
- `9900` Unexpected error. 
- `9901` Unexpected error, try later. 


### /api/logout

```
$ curl https://pcogram.com/api/logout \
  -H 'Authorization: Bearer PCOGRAM-TOKEN' \
  -X POST 
```

##### Request:

No payload is expected.
 
##### Response:
 
```json
{
  "message": "See you later.",
  "data":{
    "token":"PCOGRAM-TOKEN"
  }
}
``` 

##### Errors:
 
```json
{
  "message": "Token 'PCOGRAM-TOKEN' is invalid.",
  "error": 2101
}
```

- `2101` Invalid token.
- `2102` Empty token.
- `9900` Unexpected error. 
- `9901` Unexpected error, try later. 

### /api/post

```
$ curl https://pcogram.com/api/post \
  -H 'Authorization: Bearer PCOGRAM-TOKEN' \
  -X POST \
  -d '{"message":"😊"}' 
```

##### Request:
```json
{
  "message":"😊"
}
```

- `message`:
  - single emoji or unicode grapheme.
  - can be at most 16 code-points long.
   
##### Response:

```json
{
  "message": "Posted.",
  "data":{
    "message":"😊"
  }
}
``` 

##### Errors:

 ```json
{
  "message": "Expected single emoji or a unicode grapheme with fewer than 16 code-points.",
  "error": 2200
}
```

- `2101` Invalid token.
- `2102` Empty token.
- `2200` Message length check failed.
- `2201` Rate limited, try later.
- `9900` Unexpected error. 
- `9901` Unexpected error, try later. 

### /api/posts_by_me

```
$ curl https://pcogram.com/api/posts_by_me \
  -H 'Authorization: Bearer PCOGRAM-TOKEN'
```

##### Request:

No payload expected.
   
##### Response:

```json
{
  "message": "",
  "data":{
    "username":"batman",
    "posts":["🦇","😀","😃","😄"],
    "last_posted_at":"3 minutes ago"
  }
}
``` 

##### Errors:

```json
{
  "message": "Token 'PCOGRAM-TOKEN' is invalid.",
  "error": 2101
}
```

- `2101` Invalid token.
- `2102` Empty token.
- `9900` Unexpected error. 
- `9901` Unexpected error, try later. 


### /api/posts_by_user

```
$ curl https://pcogram.com/api/posts_by_user \
  -H 'Authorization: Bearer PCOGRAM-TOKEN' \
  -X POST \
  -d '{"username":"joker"}' 
```

##### Request:
```json
{
  "username":"joker"
}
```

- `username`:
  - valid, existing username.

##### Response:

```json
{
  "message": "",
  "data":{
    "username":"joker",
    "posts":["🤡"],
    "last_posted_at":"6 days ago"
  }
}
``` 

##### Errors:

```json
{
  "message": "Username 'jjoker' not found.",
  "error": 2103
}
```

- `2101` Invalid token.
- `2102` Empty token.
- `2103` Username not found.
- `9900` Unexpected error. 
- `9901` Unexpected error, try later. 

### /api/follow

```
$ curl https://pcogram.com/api/follow \
  -H 'Authorization: Bearer PCOGRAM-TOKEN' \
  -X POST \
  -d '{"username":"robin"}' 
```

##### Request:
```json
{
  "username":"robin"
}
```

- `username`:
  - valid, existing username.

##### Response:

```json
{
  "message": "Followed robin.",
  "data":{
    "followed":"robin"
  }
}
``` 

##### Errors:

- `2101` Invalid token.
- `2102` Empty token.
- `2103` Username not found.
- `9900` Unexpected error. 
- `9901` Unexpected error, try later. 

### /api/unfollow

```
$ curl https://pcogram.com/api/unfollow \
  -H 'Authorization: Bearer PCOGRAM-TOKEN' \
  -X POST \
  -d '{"username":"robin"}' 
```

##### Request:
```json
{
  "username":"robin"
}
```

- `username`:
  - valid, existing username.

##### Response:

```json
{
  "message": "Unfollowed robin.",
  "data":{
    "unfollowed":"robin"
  }
}
``` 

##### Errors:

- `2101` Invalid token.
- `2102` Empty token.
- `2103` Username not found.
- `9900` Unexpected error. 
- `9901` Unexpected error, try later. 

### /api/followers

```
$ curl https://pcogram.com/api/followers \
  -H 'Authorization: Bearer PCOGRAM-TOKEN'  
```

##### Request:

No payload expected.

##### Response:

```json
{
  "message": "",
  "data":{
    "followers":["robin","joker"]
  }
}
``` 

##### Errors:

- `2101` Invalid token.
- `2102` Empty token.
- `9900` Unexpected error. 
- `9901` Unexpected error, try later. 

### /api/following

```
$ curl https://pcogram.com/api/following \
  -H 'Authorization: Bearer PCOGRAM-TOKEN'  
```

##### Request:

No payload expected.

##### Response:

```json
{
  "message": "",
  "data":{
    "following":["alfred","harvey"]
  }
}
``` 

##### Errors:

- `2101` Invalid token.
- `2102` Empty token.
- `9900` Unexpected error. 
- `9901` Unexpected error, try later. 

### /api/timeline


```
$ curl https://pcogram.com/api/timeline \
  -H 'Authorization: Bearer PCOGRAM-TOKEN'  
```

##### Request:

No payload expected.

##### Response:

```json
{
  "message": "",
  "data":{
    "timeline":[
      {
        "username":"batman",
        "follower":false,
        "following":false,
        "last_posted_at":"6 hours ago",
        "last_posted_ts":"2017-11-29 16:33:51+00:00",
        "posts":["🦇","😀","😃","😄"]
        },
      {
        "username":"alfred",
        "follower":true,
        "following":true,
        "last_posted_at":"6 hours ago",
        "last_posted_ts":"2017-11-29 16:33:51+00:00",
        "posts":["😥","😎"]
        },
      {
        "username":"harvey",
        "follower":true,
        "following":true,
        "last_posted_at":"14 hours ago",
        "last_posted_ts":"2017-11-29 08:26:25+00:00",
        "posts":["🤕"]
        }
    ]
  }
}
``` 

##### Errors:

- `2101` Invalid token.
- `2102` Empty token.
- `9900` Unexpected error. 
- `9901` Unexpected error, try later. 
