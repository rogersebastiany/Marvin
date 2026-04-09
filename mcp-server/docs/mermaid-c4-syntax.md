# Mermaid.js C4 Diagram Syntax Reference

## Diagram Types
- `C4Context` — System Context (high-level overview)
- `C4Container` — Container diagram (system decomposition)
- `C4Component` — Component diagram (container internals)
- `C4Dynamic` — Dynamic diagram (interaction sequences)
- `C4Deployment` — Deployment diagram (infrastructure)

## Elements

### People
```
Person(alias, "Label", "Description")
Person_Ext(alias, "Label", "Description")
```

### Systems
```
System(alias, "Label", "Description")
System_Ext(alias, "Label", "Description")
SystemDb(alias, "Label", "Description")
SystemQueue(alias, "Label", "Description")
```

### Containers
```
Container(alias, "Label", "Technology", "Description")
ContainerDb(alias, "Label", "Technology", "Description")
ContainerQueue(alias, "Label", "Technology", "Description")
Container_Ext(alias, "Label", "Technology", "Description")
```

### Components
```
Component(alias, "Label", "Technology", "Description")
ComponentDb(alias, "Label", "Technology", "Description")
```

### Boundaries
```
Enterprise_Boundary(alias, "Label") { ... }
System_Boundary(alias, "Label") { ... }
Container_Boundary(alias, "Label") { ... }
Boundary(alias, "Label", "Type") { ... }
```

## Relationships
```
Rel(from, to, "Label", "Technology")
Rel_U(from, to, "Label")    # Upward
Rel_D(from, to, "Label")    # Downward
Rel_L(from, to, "Label")    # Left
Rel_R(from, to, "Label")    # Right
Rel_Back(from, to, "Label")
BiRel(from, to, "Label")
```

## Styling
```
UpdateElementStyle(el, $bgColor="blue", $fontColor="white")
UpdateRelStyle(from, to, $textColor="red", $lineColor="blue")
UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

## Example: System Context
```
C4Context
    title System Context Diagram
    Person(user, "User", "End user of the system")
    System(web, "Web App", "Main application")
    System_Ext(email, "Email Service", "Sends notifications")
    Rel(user, web, "Uses", "HTTPS")
    Rel(web, email, "Sends emails", "SMTP")
```
