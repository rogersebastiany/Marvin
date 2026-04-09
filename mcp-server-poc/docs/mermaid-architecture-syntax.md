# Mermaid.js Architecture Diagram Syntax Reference

## Declaration
```
architecture-beta
```

## Groups
```
group api(cloud)[API Layer]
group db(database)[Data Layer] in api
```

## Services
```
service server1(server)[App Server]
service db1(database)[PostgreSQL] in db
```

## Junctions
```
junction junc1
junction junc2 in api
```

## Default Icons
`cloud`, `database`, `disk`, `internet`, `server`

## Connections
```
{service}:{T|B|L|R} {<}?--{>}? {T|B|L|R}:{service}
```

### Examples
```
db:R -- L:server           # Undirected
server:R --> L:gateway      # Directed right-to-left
subnet{group}:B --> T:db{group}  # Group-to-group
```

### Direction Labels
- `T` = Top, `B` = Bottom, `L` = Left, `R` = Right

## Full Example
```
architecture-beta
    group api(cloud)[API]
        service gateway(internet)[Gateway]
        service app(server)[App Server]
        service db(database)[Database]

    gateway:R --> L:app
    app:R --> L:db
```
