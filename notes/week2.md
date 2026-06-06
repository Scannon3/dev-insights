1. Walk through what happens, step by step, when your code calls the Spotify API and gets data back. Where can it fail?
http request is constructed with the method,url,and auth header carrying token. spotify recieves and checks if token is valid and accurate, then responds with data. can fail if token is expired, too many requests, network isseues. proper status code will be sent back.4xx = client did something wrong. network error wont have  a code, just a timeout.
2. Why do APIs use access tokens instead of just sending your password each time?
so the password isnt exposed on the app. this tokens generate temp access without exposing password.
3. You're storing listening history. Sketch the tables and relationships. What's your reasoning for that schema?
table 1:artist. table 2: tracks(foreign key connects to artist),table 3: events(track played at this time,foreign key connects to tracks), table 4: snapshots(way to organize the insights with respect to time)
4. What does an ORM give you, and what does it hide that you should still understand?
it gives convenience and security but hides possibily inefficient code underneath. should understand exactly what each ORM query does.
5. What's the difference between data you fetch and data you derive? Where should each live?
fetched data is the data we requested through the api, derived data is what i do with it after. fetched lives in table and derived can llive in tables or can be derived on the spot through queries.