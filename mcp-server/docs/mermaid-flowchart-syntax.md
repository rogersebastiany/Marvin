# Mermaid.js Flowchart Syntax Reference

## Directions
```
flowchart TB   # Top to bottom
flowchart TD   # Top-down (same as TB)
flowchart BT   # Bottom to top
flowchart LR   # Left to right
flowchart RL   # Right to left
```

## Node Shapes
```
A                        # Default rectangle
A["Text Label"]          # Rectangle with custom text
A(Round edges)           # Rounded rectangle
A([Stadium shape])       # Stadium/pill shape
A[[Subroutine]]          # Subroutine shape
A[(Cylinder)]            # Cylinder/database
A((Circle))              # Circle
A{Rhombus}               # Diamond decision
A{{Hexagon}}             # Hexagon
A[/Parallelogram/]       # Parallelogram
A(((Double circle)))     # Double circle
```

## Edge Types
```
A --> B                  # Arrow head
A --- B                  # Open link
A -->|text| B            # Arrow with label
A -.-> B                 # Dotted arrow
A ==> B                  # Thick arrow
A ~~~ B                  # Invisible link
A --o B                  # Circle edge
A --x B                  # Cross edge
A <--> B                 # Bidirectional
```

## Subgraphs
```
subgraph id[Title]
    direction LR
    A --> B
end
```

## Styling
```
classDef myClass fill:#f9f,stroke:#333,stroke-width:4px;
class A myClass;
A:::myClass
```
