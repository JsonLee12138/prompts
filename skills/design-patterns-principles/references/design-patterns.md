# Design Patterns (GoF 23 + Common Concurrency/Enterprise Patterns)

This document includes the GoF 23 design patterns plus common concurrency/parallel and enterprise application patterns. Each entry includes: Definition, Use Cases, Pros, Cons, Typical Implementation.

## GoF Creational

**Abstract Factory**  
Definition: Provide an interface for creating families of related or dependent objects without specifying their concrete classes.  
Use Cases:  
- Need to create a family of related objects  
- Need to switch between multiple product families  
Pros:  
- Isolates concrete classes  
- Easy to switch product families  
Cons:  
- Hard to add new product types  
Typical Implementation: Abstract factory interface + concrete factories + product interfaces.

**Factory Method**  
Definition: Define an interface for creating an object, letting subclasses decide which class to instantiate.  
Use Cases:  
- Defer creation to subclasses  
- Choose implementations based on configuration  
Pros:  
- Decouples creation from use  
- Easy to extend  
Cons:  
- More classes and hierarchy  
Typical Implementation: Abstract factory method + concrete creator subclasses.

**Builder**  
Definition: Separate the construction of a complex object from its representation.  
Use Cases:  
- Many constructor parameters  
- Variable construction steps  
Pros:  
- Step-by-step construction  
- Clear build process  
Cons:  
- Extra Builder classes  
Typical Implementation: Builder interface + ConcreteBuilder + Director.

**Prototype**  
Definition: Create new objects by cloning existing instances.  
Use Cases:  
- High creation cost  
- Many similar objects  
Pros:  
- Efficient creation  
Cons:  
- Deep copy complexity  
Typical Implementation: Cloneable interface + prototype registry.

**Singleton**  
Definition: Ensure a class has only one instance and provide a global access point.  
Use Cases:  
- Shared resource management  
- Configuration registry  
Pros:  
- Controlled access  
Cons:  
- Hidden dependencies  
- Harder to test  
Typical Implementation: Private constructor + static instance + thread safety control.

## GoF Structural

**Adapter**  
Definition: Convert the interface of a class into another interface clients expect.  
Use Cases:  
- Legacy interface compatibility  
- Third-party API mismatch  
Pros:  
- Reuse existing code  
Cons:  
- Extra adaptation layer  
Typical Implementation: Target interface + adapter wrapping the legacy implementation.

**Bridge**  
Definition: Decouple an abstraction from its implementation so both can vary independently.  
Use Cases:  
- Multiple dimensions of change  
- Avoid subclass explosion  
Pros:  
- Flexible extension  
Cons:  
- More abstraction layers  
Typical Implementation: Abstraction holds a reference to an implementation interface.

**Composite**  
Definition: Compose objects into tree structures to represent part-whole hierarchies.  
Use Cases:  
- Treat single objects and composites uniformly  
Pros:  
- Simplifies client logic  
Cons:  
- Can become complex if boundaries are unclear  
Typical Implementation: Component interface + leaf and composite nodes.

**Decorator**  
Definition: Attach additional responsibilities to objects dynamically.  
Use Cases:  
- Runtime feature extension  
Pros:  
- Flexible composition over inheritance  
Cons:  
- Many layers can be hard to debug  
Typical Implementation: Component interface + decorator wrappers.

**Facade**  
Definition: Provide a unified interface to a set of interfaces in a subsystem.  
Use Cases:  
- Simplify complex subsystem usage  
Pros:  
- Reduces coupling  
Cons:  
- Can become an overly centralized entry point  
Typical Implementation: Facade class that coordinates subsystems.

**Flyweight**  
Definition: Share fine-grained objects to reduce memory usage.  
Use Cases:  
- Large numbers of similar objects  
Pros:  
- Memory savings  
Cons:  
- Complex state management  
Typical Implementation: Flyweight factory + separation of intrinsic/extrinsic state.

**Proxy**  
Definition: Provide a surrogate to control access to another object.  
Use Cases:  
- Lazy loading  
- Access control  
- Remote calls  
Pros:  
- Controlled access  
Cons:  
- Additional indirection  
Typical Implementation: Proxy implements the same interface and wraps the real object.

## GoF Behavioral

**Chain of Responsibility**  
Definition: Give multiple objects a chance to handle a request by passing it along a chain.  
Use Cases:  
- Handler not fixed at compile time  
Pros:  
- Decouples sender and receiver  
Cons:  
- Request may be unhandled  
Typical Implementation: Handler holds reference to next handler.

**Command**  
Definition: Encapsulate a request as an object for queuing, logging, and undo.  
Use Cases:  
- Undo/redo  
- Command logging  
Pros:  
- Decouples invoker and executor  
Cons:  
- Many command classes  
Typical Implementation: Command interface + Receiver + Invoker.

**Interpreter**  
Definition: Define a grammar and an interpreter for a language.  
Use Cases:  
- Rule/expression evaluation  
Pros:  
- Easy to extend grammar  
Cons:  
- Hard to maintain for complex grammars  
Typical Implementation: AST + interpretation context.

**Iterator**  
Definition: Provide a uniform way to traverse a collection.  
Use Cases:  
- Traversing complex collections  
Pros:  
- Separates traversal logic  
Cons:  
- Overkill for simple collections  
Typical Implementation: Iterator interface + collection implementation.

**Mediator**  
Definition: Encapsulate how a set of objects interact.  
Use Cases:  
- Complex interactions among many objects  
Pros:  
- Reduces coupling  
Cons:  
- Mediator can grow large  
Typical Implementation: Mediator coordinates multiple components.

**Memento**  
Definition: Capture and externalize an object's internal state without violating encapsulation.  
Use Cases:  
- State restore  
- Undo operations  
Pros:  
- Preserves encapsulation  
Cons:  
- Extra storage cost  
Typical Implementation: Originator + Memento + Caretaker.

**Observer**  
Definition: Define a one-to-many dependency so observers are notified of changes.  
Use Cases:  
- Event-driven systems  
Pros:  
- Decouples subject and observers  
Cons:  
- Notification chains are hard to trace  
Typical Implementation: Subject maintains an observer list.

**State**  
Definition: Encapsulate state-specific behavior and switch behavior by changing state.  
Use Cases:  
- Behavior varies by state  
Pros:  
- Eliminates large conditionals  
Cons:  
- Many state classes  
Typical Implementation: Context holds a State.

**Strategy**  
Definition: Define a family of algorithms, encapsulate each, and make them interchangeable.  
Use Cases:  
- Switch algorithms at runtime  
Pros:  
- Easy to extend  
Cons:  
- Many strategy classes  
Typical Implementation: Strategy interface + multiple implementations.

**Template Method**  
Definition: Define the skeleton of an algorithm, letting subclasses redefine steps.  
Use Cases:  
- Fixed process with variable steps  
Pros:  
- Reuse the overall flow  
Cons:  
- Inheritance-based  
Typical Implementation: Abstract class with a template method.

**Visitor**  
Definition: Separate operations from an object structure.  
Use Cases:  
- Stable object structure, frequently changing operations  
Pros:  
- Easy to add new operations  
Cons:  
- Hard to add new element types  
Typical Implementation: Visitor interface + Element interface.

## Common Concurrency/Parallel Patterns

**Thread Pool**  
Definition: Reuse a pool of threads to execute tasks.  
Use Cases:  
- High-concurrency task execution  
Pros:  
- Resource control  
Cons:  
- Queue congestion risk  
Typical Implementation: Task queue + fixed thread pool.

**Producer-Consumer**  
Definition: Coordinate producers and consumers via a buffer.  
Use Cases:  
- Asynchronous task processing  
Pros:  
- Decouples production and consumption  
Cons:  
- Synchronization required  
Typical Implementation: Blocking queue + producer/consumer threads.

**Event Loop**  
Definition: Single-threaded loop that processes events from a queue.  
Use Cases:  
- I/O-bound workloads  
Pros:  
- Low thread overhead  
Cons:  
- CPU-bound tasks can block  
Typical Implementation: Event queue + callbacks/task scheduler.

**Reactor**  
Definition: An event dispatcher that demultiplexes and dispatches events to handlers.  
Use Cases:  
- High-concurrency network I/O  
Pros:  
- Scalable  
Cons:  
- Callback complexity  
Typical Implementation: Selector + Handlers.

**Proactor**  
Definition: Asynchronous I/O with completion callbacks.  
Use Cases:  
- Platforms with async I/O support  
Pros:  
- Leverages OS async I/O  
Cons:  
- Platform-dependent  
Typical Implementation: Async I/O + completion handlers.

**Active Object**  
Definition: Invoke object methods asynchronously via a message queue.  
Use Cases:  
- Thread-safe method invocation  
Pros:  
- Simplifies concurrency control  
Cons:  
- Harder to debug  
Typical Implementation: Proxy + request queue + worker thread.

**Future/Promise**  
Definition: Represents a result that will be available later.  
Use Cases:  
- Asynchronous programming  
Pros:  
- Compose async tasks  
Cons:  
- Complex error propagation  
Typical Implementation: Future object + callbacks/await.

**Read-Write Lock**  
Definition: Allows concurrent reads but exclusive writes.  
Use Cases:  
- Read-heavy workloads  
Pros:  
- Better read throughput  
Cons:  
- Writer starvation risk  
Typical Implementation: Read-write lock mechanism.

**Monitor Object**  
Definition: Encapsulate synchronization within an object.  
Use Cases:  
- Shared resources in multi-threading  
Pros:  
- Safe access control  
Cons:  
- Potential blocking  
Typical Implementation: Internal lock + condition variables.

**Leader-Followers**  
Definition: One leader thread handles events, then hands off leadership to another thread.  
Use Cases:  
- High-concurrency event dispatching  
Pros:  
- Fewer thread context switches  
Cons:  
- Complex implementation  
Typical Implementation: Thread pool + leader election.

**Half-Sync/Half-Async**  
Definition: Asynchronously accept requests, synchronously process tasks.  
Use Cases:  
- High request volume with synchronous processing  
Pros:  
- Balances throughput and control  
Cons:  
- Complex structure  
Typical Implementation: Async acceptor + synchronous worker pool.

## Common Enterprise Application Patterns

**Repository**  
Definition: Abstract data access behind a repository.  
Use Cases:  
- Decouple domain model from data access  
Pros:  
- Hides data details  
Cons:  
- Risk of over-abstraction  
Typical Implementation: Repository interface + ORM implementation.

**Unit of Work**  
Definition: Track a set of operations as a single transaction.  
Use Cases:  
- Consistent commit across multiple entities  
Pros:  
- Unified transaction management  
Cons:  
- Complex implementation  
Typical Implementation: Change tracking + commit/rollback.

**Data Mapper**  
Definition: Separate in-memory objects from database tables.  
Use Cases:  
- Rich domain model  
Pros:  
- Domain model independence  
Cons:  
- Mapping code overhead  
Typical Implementation: Mapper classes + data access layer.

**Active Record**  
Definition: Domain object contains persistence logic.  
Use Cases:  
- Simple CRUD applications  
Pros:  
- Simple to implement  
Cons:  
- Coupled business and persistence logic  
Typical Implementation: Model.save/update/delete.

**DAO (Data Access Object)**  
Definition: Encapsulate data access and provide a uniform interface.  
Use Cases:  
- Multiple data sources  
Pros:  
- Isolated data access layer  
Cons:  
- Can become anemic  
Typical Implementation: DAO interface + SQL/ORM implementation.

**Service Layer**  
Definition: Encapsulate application use cases in a service layer.  
Use Cases:  
- Complex business workflows  
Pros:  
- Unified business entry points  
Cons:  
- Risk of god services  
Typical Implementation: Application service + use case methods.

**Domain Model**  
Definition: Center the system around domain objects and behavior.  
Use Cases:  
- Complex business rules  
Pros:  
- Clear semantics  
Cons:  
- Higher design cost  
Typical Implementation: Aggregates + value objects + domain services.

**Transaction Script**  
Definition: Organize business logic as procedural scripts.  
Use Cases:  
- Simple business rules  
Pros:  
- Fast to implement  
Cons:  
- Hard to scale/extend  
Typical Implementation: Single service method for a full use case.

**Table Module**  
Definition: One class handles the business logic for all rows in a table.  
Use Cases:  
- Table-centric systems  
Pros:  
- Direct implementation  
Cons:  
- Limited OO expressiveness  
Typical Implementation: Table object + row operations.

**DTO (Data Transfer Object)**  
Definition: Simple objects for transferring data across layers/services.  
Use Cases:  
- API transfer objects  
Pros:  
- Reduced network overhead  
Cons:  
- Object bloat risk  
Typical Implementation: Plain data structure + serialization.

**Identity Map**  
Definition: Cache loaded objects to ensure identity uniqueness.  
Use Cases:  
- Complex object loading  
Pros:  
- Avoid duplicate loads  
Cons:  
- Memory overhead  
Typical Implementation: Map cache + identity control.

**Lazy Load**  
Definition: Load object data on demand.  
Use Cases:  
- Large datasets  
Pros:  
- Improved performance  
Cons:  
- Potential N+1 queries  
Typical Implementation: Proxy object + deferred query.

**Specification**  
Definition: Encapsulate business rules as composable specifications.  
Use Cases:  
- Complex filtering conditions  
Pros:  
- Rule reuse  
Cons:  
- Abstraction complexity  
Typical Implementation: Specification interface + rule composition.
