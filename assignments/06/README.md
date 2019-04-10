# TODO Protocol

The server maintains a todo file with todo items.
The server's client handling is multithreaded so multiple clients are allowed.
When the threads are accessing the todo file for read/write purposes, the file is locked in order to avoid a data race.

A multithreaded server is important because the server is not blocked while a single client connection is handled.
Implementing mutual exclusion to the todo file is important because the client threads cannot write to it simultaneously.
The reading of the todo file also requires a lock in order to avoid dirty reads should a client thread modify the file at the same time.
When a thread acquires the lock then the thread sleeps for 5 seconds.
This way it can be easily proved that other threads are blocked until the lock is released.

Logging is used to prove that the mutex works as intended.
See [debug log](debug.log) for logging information about how the threads manage the lock.
For example, thread 2 acquires the lock and thread 3 is trying to get it.
Thread 3 has to wait until thread 2 is done with the lock.

[Specification of the protocol](spec.md) is available. The spec is based on assignment 4's spec.

Different example [request-response outputs](outputs.md) are available.

## Example usage

Example usage of the client: python client.py localhost 8888 "LIST 0 ."

Example usage of the server: python server.py localhost 8888

Author: [Hannu Oksman](https://student.labranet.jamk.fi/~L2912/)
