# Sales Ape Interview Task

## Running the App

* Add your `OPENAI_API_KEY` to .env.
* Ensure docker and docker compose installed.
* Run (apologies frontend image takes a while to build:

```
> make start

```

* Frontend runs on localhost:8080 by default


## Functionality

* User connects their Spotify account
* The user is prompted for input
* The default response is a song recommendation (the current implementation does not support general chat, so each response will be a recommendation)
* The user can continue to provide feedback or clarify their feelings and preferences to receive updated recommendations
* If the user enters "play" after a recommendation, they will be redirected to the song on Spotify

## Implementation Details

* Spotify API
  - The recommendations use the audio features of each track
  - Originally planned to retrieve the user's next recommended tracks as input, but the audio features Spotify endpoint has been deprecated
  - Instead used a [`Hugging Face dataset`](./backend/src/spotify/spotify_tracks_top_10000.csv) with track audio features, with the data stored in [SQLite DB](./backend/src/spotify/tables.py)
  - For each round of recommendations, this DB is [randomly sampled](./backend/src/api/routes/chat.py#L32) for 30 tracks which are used as the candidates to be passed to the prompt

* Burr State Machine
  - The agent itself is implemented using the [Burr library](https://burr.dagworks.io/)
  - Key code components are:
    - [Actions](./backend/src/ai/nodes.py): functions to run at each node of the graph are defined
    - [Burr app](./backend/src/ai/state_machine.py): defines the actions (nodes) and possible transitions

* Chat Endpoint
  - All chat requests go via [this endpoint](./backend/src/api/routes/chat.py#L30)
  - Manages control flow of state machine, yielding back to client for user input
  - Returns one of a number of events for the client to process (websocket would be better here, see below)

## Future Improvements

* General Chat and LLM Decision Making
  - Update the state machine to have general chat with recommendation function and play track options provided as "tools" for the LLM
  - Use the LLM to decide what step to perform next (instead of hard coding logic as in current implementation)

* Websocket
  - Using REST API to return different event objects is not desirable
  - Using a websocket instead would be preferable for sending events to the client
  - Prevents long running requests (server -> client communication)
  - Lends itself to growing number of events which could be handled uniquely by client, e.g.:
    - Simple text chat event - initiate raw text streamed to client
    - Recommendation event - could include album artwork, song preview and rendered by specific UI component
    - Redirect event

* Asyncio
  - All libraries used support async, which allows parallel long running I/O, important for LLM requests
