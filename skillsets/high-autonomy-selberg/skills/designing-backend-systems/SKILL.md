---
name: designing-backend-systems
description: Use when designing a backend system architecture. For example, use this skill when thinking about how to implement backend state, how to integrate with an API, or how to wire together multiple backend services.
---

<required>
CRITICAL. Add the following steps to your task list:

1. Read the system design principles below as context for any other tasks.

</required>

# System Design Principles

<system-reminder> This system design assumes an express typescript application, but the same principles should apply across many kinds of codebases. </system-reminder>

Folder structure:
```
server.ts  # Express server setup.  Initilizes all providers and persistence classes, and all routers.
env.ts  # Maps all environment variables to actual variables.
runtime.ts  # A singleton class that contains references to providers and persistence singleton classes.
mocktime.ts  # A singleton class that contains references to mock providers and persistence singleton classes. A 1:1 mock of the runtime.
endpoints/  # All inbound endpoints to the server.
  public/
    foo/  # Each endpoint type is stored in a folder grouped by concept name. Every endpoint folder contains a routes.ts that contains an exported router that allows registering endpoints.
      routes.ts  # For long-running endpoints that require more than an http round trip, routes.ts contains thin wrappers that delegate to handlers.ts.
      handlers.ts  # Handlers for long-running tasks.
    bar/
      routes.ts  # For simple CRUD tasks, routes.ts handles everything, no handlers.ts.
    ...
  authenticated/  # Any endpoints that require auth middleware.
    foo/
      routes.ts
      handlers.ts
    baz/
      routes.ts
    ...
middleware/
  auth.ts
  errorHandling.ts
  ...
features/  # Contains most business logic, separated into folders by feature name.
  foo/
    fooPipeline.ts
    fooAnalysis.ts
  bar/
    barBroadcast.ts
  ...
persistence/  # Contains all singleton classes for storing data into persistence.
  User.ts
  DataStructure.ts
  ...
providers/  # Singleton classes for all interactions with third party libraries.
  aws.ts
  firebase.ts
  openai.ts
  ...
lib/  # Any code that does NOT have business logic.
  validation.ts
  errors.ts
  ...
```

runtime:
- a runtime is a singleton class that contains lazy references to anything in providers and persistence
- the point of the runtime is to centralize a single passed-around object that can be used as a parameter for server-wide logic
- the runtime should be initialized in server.ts, passed in or loaded in any endpoint that needs it, and then passed through downstream calls
- assume any reference to calling persistence or providers below goes through runtime
- the mocktime is a closely related concept -- any provider/persistence class should contain a mock, which can be referenced in the mocktime as a dropin replacement

endpoints:
- endpoints are separated into folders
- each folder has a routes.ts file containing all of the endpoints in that folder
- each folder is named by concept
  - folders can be named after data structures (e.g. user), and the routes.ts contains CRUD endpoints
  - folders can be named after clusters of actions (e.g. analytics) and the routes.ts contains bespoke endpoints for that set of actions
- routes that take longer than an HTTP request should call out to an async function in a handlers.ts file in the same folder
  - in this setting, the route itself returns a unique key that the client can query to an external persisted location
  - the handler would then write some response to that location in an async fashion
  - see 'Message Bus' below
- CRUD endpoints call to the persistence layer
- everything else calls into the features layer

middleware:
- middleware runs on every endpoint call
- generally used for logs, auth, and error handling

features:
- business logic is grouped by semantic 'feature' in named subfolders
- anything that is not crud logic should go in features/, including anything that requires stiching together multiple provider/persistence calls

persistence:
- where server types are defined and CRUD is set up
- persistence wraps over one or more providers, generally databases and blobstores
- each file in persistence is named for and references a single data structure, e.g. Foo.ts would define type Foo
- the persistence file defines a singleton class that in turn instantiates a connection to an underlying provider
- the singleton class should define CRUD methods
- optionally, the persistence file can contain pure function helpers for common server-specific semantics outside of the singleton class
<system-note> we recommend a single list function that can be parameterized with any query logic necessary, including `limit` or `page`. The persistence file can export a type, FooQueryArgs, that simply exports the available queryable fields and their types. </system-note>

providers:
- abstractions over third party libraries or first party isolated modules
- very little business logic lives in providers
- providers are singleton classes that set up and manage the lifecycle of third party connections
- it can be useful to create first party providers when they can be isolated
  - for example: a fs-json provider that exposes CRUD operations over a simple on-disk json file
- each provider is named for what it abstracts, e.g. sqlite.ts, aws.ts, etc.

lib:
- code that has 0 unique business logic whatsoever
- these are utilities that can be pulled out from the codebase and dropped in elsewhere
- any language-specific utilities (e.g. status monads, function parameter default conventions, etc.) belong in lib/

# Common patterns

## Message Bus
- Used for long running async tasks where the client may not get a response for tens of minutes (i.e. outside HTTP timeouts)
- server endpoint returns a unique id immediately to the client, then passes that unique id to a long running worker process
- the worker process eventually stores the result of its work in a side channel db (optionally with a ttl)
- the client receives the unique id and polls the side channel db (or registers a server-side event listener or socket listener)
- once the side channel db gets data with the unique id, the client can pick it up

The message bus pattern can be used as a central comms store for many different components in a system.

## Worker Queue
- Used to handle bursty load with limited resources
- server endpoint is a thin layer that just stores a task on a queue (SQS, Kafka, RabbitMQ)
  - the task is an rpc -- it defines a function and some parameters
- separately, a set of workers read from the queue on repeat
  - workers may live on the same machine as different processes / threads, or on different machines entirely
  - each cycle, the worker process takes from the queue, switch-statements the task, and handles it
  - when completed, the work is often written to a third party location
