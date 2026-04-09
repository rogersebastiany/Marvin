# Mermaid.js Sequence Diagram Syntax Reference

## Participants
```
sequenceDiagram
    participant A
    participant B as Alias Name
    actor User
```

## Messages
```
A->B: Solid line
A-->B: Dotted line
A->>B: Solid with arrowhead
A-->>B: Dotted with arrowhead
A-xB: Cross end (sync lost)
A-)B: Async open arrow
```

## Activations
```
activate A
deactivate A
A->>+B: Activate shorthand
B-->>-A: Deactivate shorthand
```

## Notes
```
Note right of A: Text
Note left of B: Text
Note over A,B: Spanning note
```

## Control Flow
```
loop Every minute
    A->>B: Health check
end

alt Success
    B-->>A: 200 OK
else Failure
    B-->>A: 500 Error
end

opt Optional
    A->>B: Extra call
end

par Parallel 1
    A->>B: Request 1
and Parallel 2
    A->>C: Request 2
end
```

## Boxes / Grouping
```
box Purple "Backend Services"
    participant API
    participant DB
end
```
