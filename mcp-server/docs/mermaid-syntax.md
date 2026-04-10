# Mermaid.js Diagram Syntax


---

## 1. Flowcharts - Basic Syntax

Flowcharts are composed of **nodes** (geometric shapes) and **edges** (arrows or lines). The Mermaid code defines how nodes and edges are made and accommodates different arrow types, multi-directional arrows, and any linking to and from subgraphs.

WARNING

If you are using the word "end" in a Flowchart node, capitalize the entire word or any of the letters (e.g., "End" or "END"), or apply this [workaround](https://github.com/mermaid-js/mermaid/issues/1444#issuecomment-639528897). Typing "end" in all lowercase letters will break the Flowchart.

WARNING

If you are using the letter "o" or "x" as the first letter in a connecting Flowchart node, add a space before the letter or capitalize the letter (e.g., "dev--- ops", "dev---Ops").

Typing "A---oB" will create a [circle edge](#circle-edge-example).

Typing "A---xB" will create a [cross edge](#cross-edge-example).

### A node (default)

##### Code:

mermaid

Ctrl + Enter|

INFO

The id is what is displayed in the box.

TIP

Instead of `flowchart` one can also use `graph`.

### A node with text

It is also possible to set text in the box that differs from the id. If this is done several times, it is the last text found for the node that will be used. Also if you define edges for the node later on, you can omit text definitions. The one previously defined will be used when rendering the box.

##### Code:

mermaid

Ctrl + Enter|

#### Unicode text

Use `"` to enclose the unicode text.

##### Code:

mermaid

Ctrl + Enter|

#### Markdown formatting

Use double quotes and backticks "` text `" to enclose the markdown text.

##### Code:

mermaid

Ctrl + Enter|

### Direction

This statement declares the direction of the Flowchart.

This declares the flowchart is oriented from top to bottom (`TD` or `TB`).

##### Code:

mermaid

Ctrl + Enter|

This declares the flowchart is oriented from left to right (`LR`).

##### Code:

mermaid

Ctrl + Enter|

Possible FlowChart orientations are:

* TB - Top to bottom
* TD - Top-down/ same as top to bottom
* BT - Bottom to top
* RL - Right to left
* LR - Left to right

## Node shapes

### A node with round edges

##### Code:

mermaid

Ctrl + Enter|

### A stadium-shaped node

##### Code:

mermaid

Ctrl + Enter|

### A node in a subroutine shape

##### Code:

mermaid

Ctrl + Enter|

### A node in a cylindrical shape

##### Code:

mermaid

Ctrl + Enter|

### A node in the form of a circle

##### Code:

mermaid

Ctrl + Enter|

### A node in an asymmetric shape

##### Code:

mermaid

Ctrl + Enter|

Currently only the shape above is possible and not its mirror. *This might change with future releases.*

### A node (rhombus)

##### Code:

mermaid

Ctrl + Enter|

### A hexagon node

##### Code:

mermaid

Ctrl + Enter|

### Parallelogram

##### Code:

mermaid

Ctrl + Enter|

### Parallelogram alt

##### Code:

mermaid

Ctrl + Enter|

### Trapezoid

##### Code:

mermaid

Ctrl + Enter|

### Trapezoid alt

##### Code:

mermaid

Ctrl + Enter|

### Double circle

##### Code:

mermaid

Ctrl + Enter|

## Expanded Node Shapes in Mermaid Flowcharts (v11.3.0+)

Mermaid introduces 30 new shapes to enhance the flexibility and precision of flowchart creation. These new shapes provide more options to represent processes, decisions, events, data storage visually, and other elements within your flowcharts, improving clarity and semantic meaning.

New Syntax for Shape Definition

Mermaid now supports a general syntax for defining shape types to accommodate the growing number of shapes. This syntax allows you to assign specific shapes to nodes using a clear and flexible format:

```
A@{ shape: rect }
```

This syntax creates a node A as a rectangle. It renders in the same way as `A["A"]`, or `A`.

### Complete List of New Shapes

Below is a comprehensive list of the newly introduced shapes and their corresponding semantic meanings, short names, and aliases:

| **Semantic Name** | **Shape Name** | **Short Name** | **Description** | **Alias Supported** |
| --- | --- | --- | --- | --- |
| Bang | Bang | `bang` | Bang | `bang` |
| Card | Notched Rectangle | `notch-rect` | Represents a card | `card`, `notched-rectangle` |
| Cloud | Cloud | `cloud` | cloud | `cloud` |
| Collate | Hourglass | `hourglass` | Represents a collate operation | `collate`, `hourglass` |
| Com Link | Lightning Bolt | `bolt` | Communication link | `com-link`, `lightning-bolt` |
| Comment | Curly Brace | `brace` | Adds a comment | `brace-l`, `comment` |
| Comment Right | Curly Brace | `brace-r` | Adds a comment |  |
| Comment with braces on both sides | Curly Braces | `braces` | Adds a comment |  |
| Data Input/Output | Lean Right | `lean-r` | Represents input or output | `in-out`, `lean-right` |
| Data Input/Output | Lean Left | `lean-l` | Represents output or input | `lean-left`, `out-in` |
| Database | Cylinder | `cyl` | Database storage | `cylinder`, `database`, `db` |
| Decision | Diamond | `diam` | Decision-making step | `decision`, `diamond`, `question` |
| Delay | Half-Rounded Rectangle | `delay` | Represents a delay | `half-rounded-rectangle` |
| Direct Access Storage | Horizontal Cylinder | `h-cyl` | Direct access storage | `das`, `horizontal-cylinder` |
| Disk Storage | Lined Cylinder | `lin-cyl` | Disk storage | `disk`, `lined-cylinder` |
| Display | Curved Trapezoid | `curv-trap` | Represents a display | `curved-trapezoid`, `display` |
| Divided Process | Divided Rectangle | `div-rect` | Divided process shape | `div-proc`, `divided-process`, `divided-rectangle` |
| Document | Document | `doc` | Represents a document | `doc`, `document` |
| Event | Rounded Rectangle | `rounded` | Represents an event | `event` |
| Extract | Triangle | `tri` | Extraction process | `extract`, `triangle` |
| Fork/Join | Filled Rectangle | `fork` | Fork or join in process flow | `join` |
| Internal Storage | Window Pane | `win-pane` | Internal storage | `internal-storage`, `window-pane` |
| Junction | Filled Circle | `f-circ` | Junction point | `filled-circle`, `junction` |
| Lined Document | Lined Document | `lin-doc` | Lined document | `lined-document` |
| Lined/Shaded Process | Lined Rectangle | `lin-rect` | Lined process shape | `lin-proc`, `lined-process`, `lined-rectangle`, `shaded-process` |
| Loop Limit | Trapezoidal Pentagon | `notch-pent` | Loop limit step | `loop-limit`, `notched-pentagon` |
| Manual File | Flipped Triangle | `flip-tri` | Manual file operation | `flipped-triangle`, `manual-file` |
| Manual Input | Sloped Rectangle | `sl-rect` | Manual input step | `manual-input`, `sloped-rectangle` |
| Manual Operation | Trapezoid Base Top | `trap-t` | Represents a manual task | `inv-trapezoid`, `manual`, `trapezoid-top` |
| Multi-Document | Stacked Document | `docs` | Multiple documents | `documents`, `st-doc`, `stacked-document` |
| Multi-Process | Stacked Rectangle | `st-rect` | Multiple processes | `processes`, `procs`, `stacked-rectangle` |
| Odd | Odd | `odd` | Odd shape |  |
| Paper Tape | Flag | `flag` | Paper tape | `paper-tape` |
| Prepare Conditional | Hexagon | `hex` | Preparation or condition step | `hexagon`, `prepare` |
| Priority Action | Trapezoid Base Bottom | `trap-b` | Priority action | `priority`, `trapezoid`, `trapezoid-bottom` |
| Process | Rectangle | `rect` | Standard process shape | `proc`, `process`, `rectangle` |
| Start | Circle | `circle` | Starting point | `circ` |
| Start | Small Circle | `sm-circ` | Small starting point | `small-circle`, `start` |
| Stop | Double Circle | `dbl-circ` | Represents a stop point | `double-circle` |
| Stop | Framed Circle | `fr-circ` | Stop point | `framed-circle`, `stop` |
| Stored Data | Bow Tie Rectangle | `bow-rect` | Stored data | `bow-tie-rectangle`, `stored-data` |
| Subprocess | Framed Rectangle | `fr-rect` | Subprocess | `framed-rectangle`, `subproc`, `subprocess`, `subroutine` |
| Summary | Crossed Circle | `cross-circ` | Summary | `crossed-circle`, `summary` |
| Tagged Document | Tagged Document | `tag-doc` | Tagged document | `tag-doc`, `tagged-document` |
| Tagged Process | Tagged Rectangle | `tag-rect` | Tagged process | `tag-proc`, `tagged-process`, `tagged-rectangle` |
| Terminal Point | Stadium | `stadium` | Terminal point | `pill`, `terminal` |
| Text Block | Text Block | `text` | Text block |  |

### Example Flowchart with New Shapes

Here’s an example flowchart that utilizes some of the newly introduced shapes:

##### Code:

mermaid

Ctrl + Enter|

### Process

##### Code:

mermaid

Ctrl + Enter|

### Event

##### Code:

mermaid

Ctrl + Enter|

### Terminal Point (Stadium)

##### Code:

mermaid

Ctrl + Enter|

### Subprocess

##### Code:

mermaid

Ctrl + Enter|

### Database (Cylinder)

##### Code:

mermaid

Ctrl + Enter|

### Start (Circle)

##### Code:

mermaid

Ctrl + Enter|

### Odd

##### Code:

mermaid

Ctrl + Enter|

### Decision (Diamond)

##### Code:

mermaid

Ctrl + Enter|

### Prepare Conditional (Hexagon)

##### Code:

mermaid

Ctrl + Enter|

### Data Input/Output (Lean Right)

##### Code:

mermaid

Ctrl + Enter|

### Data Input/Output (Lean Left)

##### Code:

mermaid

Ctrl + Enter|

### Priority Action (Trapezoid Base Bottom)

##### Code:

mermaid

Ctrl + Enter|

### Manual Operation (Trapezoid Base Top)

##### Code:

mermaid

Ctrl + Enter|

### Stop (Double Circle)

##### Code:

mermaid

Ctrl + Enter|

### Text Block

##### Code:

mermaid

Ctrl + Enter|

### Card (Notched Rectangle)

##### Code:

mermaid

Ctrl + Enter|

### Lined/Shaded Process

##### Code:

mermaid

Ctrl + Enter|

### Start (Small Circle)

##### Code:

mermaid

Ctrl + Enter|

### Stop (Framed Circle)

##### Code:

mermaid

Ctrl + Enter|

### Fork/Join (Long Rectangle)

##### Code:

mermaid

Ctrl + Enter|

### Collate (Hourglass)

##### Code:

mermaid

Ctrl + Enter|

### Comment (Curly Brace)

##### Code:

mermaid

Ctrl + Enter|

### Comment Right (Curly Brace Right)

##### Code:

mermaid

Ctrl + Enter|

### Comment with braces on both sides

##### Code:

mermaid

Ctrl + Enter|

### Com Link (Lightning Bolt)

##### Code:

mermaid

Ctrl + Enter|

### Document

##### Code:

mermaid

Ctrl + Enter|

### Delay (Half-Rounded Rectangle)

##### Code:

mermaid

Ctrl + Enter|

### Direct Access Storage (Horizontal Cylinder)

##### Code:

mermaid

Ctrl + Enter|

### Disk Storage (Lined Cylinder)

##### Code:

mermaid

Ctrl + Enter|

### Display (Curved Trapezoid)

##### Code:

mermaid

Ctrl + Enter|

### Divided Process (Divided Rectangle)

##### Code:

mermaid

Ctrl + Enter|

### Extract (Small Triangle)

##### Code:

mermaid

Ctrl + Enter|

### Internal Storage (Window Pane)

##### Code:

mermaid

Ctrl + Enter|

### Junction (Filled Circle)

##### Code:

mermaid

Ctrl + Enter|

### Lined Document

##### Code:

mermaid

Ctrl + Enter|

### Loop Limit (Notched Pentagon)

##### Code:

mermaid

Ctrl + Enter|

### Manual File (Flipped Triangle)

##### Code:

mermaid

Ctrl + Enter|

### Manual Input (Sloped Rectangle)

##### Code:

mermaid

Ctrl + Enter|

### Multi-Document (Stacked Document)

##### Code:

mermaid

Ctrl + Enter|

### Multi-Process (Stacked Rectangle)

##### Code:

mermaid

Ctrl + Enter|

### Paper Tape (Flag)

##### Code:

mermaid

Ctrl + Enter|

### Stored Data (Bow Tie Rectangle)

##### Code:

mermaid

Ctrl + Enter|

### Summary (Crossed Circle)

##### Code:

mermaid

Ctrl + Enter|

### Tagged Document

##### Code:

mermaid

Ctrl + Enter|

### Tagged Process (Tagged Rectangle)

##### Code:

mermaid

Ctrl + Enter|

## Special shapes in Mermaid Flowcharts (v11.3.0+)

Mermaid also introduces 2 special shapes to enhance your flowcharts: **icon** and **image**. These shapes allow you to include icons and images directly within your flowcharts, providing more visual context and clarity.

### Icon Shape

You can use the `icon` shape to include an icon in your flowchart. To use icons, you need to register the icon pack first. Follow the instructions to [add custom icons](./../config/icons.html). The syntax for defining an icon shape is as follows:

##### Code:

mermaid

Ctrl + Enter|

#### Parameters

* **icon**: The name of the icon from the registered icon pack.
* **form**: Specifies the background shape of the icon. If not defined there will be no background to icon. Options include:
  + `square`
  + `circle`
  + `rounded`
* **label**: The text label associated with the icon. This can be any string. If not defined, no label will be displayed.
* **pos**: The position of the label. If not defined label will default to bottom of icon. Possible values are:
  + `t`
  + `b`
* **h**: The height of the icon. If not defined this will default to 48 which is minimum.

### Image Shape

You can use the `image` shape to include an image in your flowchart. The syntax for defining an image shape is as follows:

```
flowchart TD
    A@{ img: "https://example.com/image.png", label: "Image Label", pos: "t", w: 60, h: 60, constraint: "off" }
```

#### Parameters

* **img**: The URL of the image to be displayed.
* **label**: The text label associated with the image. This can be any string. If not defined, no label will be displayed.
* **pos**: The position of the label. If not defined, the label will default to the bottom of the image. Possible values are:
  + `t`
  + `b`
* **w**: The width of the image. If not defined, this will default to the natural width of the image.
* **h**: The height of the image. If not defined, this will default to the natural height of the image.
* **constraint**: Determines if the image should constrain the node size. This setting also ensures the image maintains its original aspect ratio, adjusting the width (`w`) accordingly to the height (`h`). If not defined, this will default to `off` Possible values are:
  + `on`
  + `off`

If you want to resize an image, but keep the same aspect ratio, set `h`, and set `constraint: on` to constrain the aspect ratio. E.g.

##### Code:

mermaid

Ctrl + Enter|

## Links between nodes

Nodes can be connected with links/edges. It is possible to have different types of links or attach a text string to a link.

### A link with arrow head

##### Code:

mermaid

Ctrl + Enter|

### An open link

##### Code:

mermaid

Ctrl + Enter|

### Text on links

##### Code:

mermaid

Ctrl + Enter|

or

##### Code:

mermaid

Ctrl + Enter|

### A link with arrow head and text

##### Code:

mermaid

Ctrl + Enter|

or

##### Code:

mermaid

Ctrl + Enter|

### Dotted link

##### Code:

mermaid

Ctrl + Enter|

### Dotted link with text

##### Code:

mermaid

Ctrl + Enter|

### Thick link

##### Code:

mermaid

Ctrl + Enter|

### Thick link with text

##### Code:

mermaid

Ctrl + Enter|

### An invisible link

This can be a useful tool in some instances where you want to alter the default positioning of a node.

##### Code:

mermaid

Ctrl + Enter|

### Chaining of links

It is possible declare many links in the same line as per below:

##### Code:

mermaid

Ctrl + Enter|

It is also possible to declare multiple nodes links in the same line as per below:

##### Code:

mermaid

Ctrl + Enter|

You can then describe dependencies in a very expressive way. Like the one-liner below:

##### Code:

mermaid

Ctrl + Enter|

If you describe the same diagram using the basic syntax, it will take four lines. A word of warning, one could go overboard with this making the flowchart harder to read in markdown form. The Swedish word `lagom` comes to mind. It means, not too much and not too little. This goes for expressive syntaxes as well.

##### Code:

mermaid

Ctrl + Enter|

### Attaching an ID to Edges

Mermaid now supports assigning IDs to edges, similar to how IDs and metadata can be attached to nodes. This feature lays the groundwork for more advanced styling, classes, and animation capabilities on edges.

**Syntax:**

To give an edge an ID, prepend the edge syntax with the ID followed by an `@` character. For example:

##### Code:

mermaid

Ctrl + Enter|

In this example, `e1` is the ID of the edge connecting `A` to `B`. You can then use this ID in later definitions or style statements, just like with nodes.

### Turning an Animation On

Once you have assigned an ID to an edge, you can turn on animations for that edge by defining the edge’s properties:

##### Code:

mermaid

Ctrl + Enter|

This tells Mermaid that the edge `e1` should be animated.

### Selecting Type of Animation

In the initial version, two animation speeds are supported: `fast` and `slow`. Selecting a specific animation type is a shorthand for enabling animation and setting the animation speed in one go.

**Examples:**

##### Code:

mermaid

Ctrl + Enter|

This is equivalent to `{ animate: true, animation: fast }`.

### Using classDef Statements for Animations

You can also animate edges by assigning a class to them and then defining animation properties in a `classDef` statement. For example:

##### Code:

mermaid

Ctrl + Enter|

In this snippet:

* `e1@-->` creates an edge with ID `e1`.
* `classDef animate` defines a class named `animate` with styling and animation properties.
* `class e1 animate` applies the `animate` class to the edge `e1`.

**Note on Escaping Commas:** When setting the `stroke-dasharray` property, remember to escape commas as `\,` since commas are used as delimiters in Mermaid’s style definitions.

## New arrow types

There are new types of arrows supported:

* circle edge
* cross edge

### Circle edge example

##### Code:

mermaid

Ctrl + Enter|

### Cross edge example

##### Code:

mermaid

Ctrl + Enter|

## Multi directional arrows

There is the possibility to use multidirectional arrows.

##### Code:

mermaid

Ctrl + Enter|

### Minimum length of a link

Each node in the flowchart is ultimately assigned to a rank in the rendered graph, i.e. to a vertical or horizontal level (depending on the flowchart orientation), based on the nodes to which it is linked. By default, links can span any number of ranks, but you can ask for any link to be longer than the others by adding extra dashes in the link definition.

In the following example, two extra dashes are added in the link from node *B* to node *E*, so that it spans two more ranks than regular links:

##### Code:

mermaid

Ctrl + Enter|

> **Note** Links may still be made longer than the requested number of ranks by the rendering engine to accommodate other requests.

When the link label is written in the middle of the link, the extra dashes must be added on the right side of the link. The following example is equivalent to the previous one:

##### Code:

mermaid

Ctrl + Enter|

For dotted or thick links, the characters to add are equals signs or dots, as summed up in the following table:

| Length | 1 | 2 | 3 |
| --- | --- | --- | --- |
| Normal | `---` | `----` | `-----` |
| Normal with arrow | `-->` | `--->` | `---->` |
| Thick | `===` | `====` | `=====` |
| Thick with arrow | `==>` | `===>` | `====>` |
| Dotted | `-.-` | `-..-` | `-...-` |
| Dotted with arrow | `-.->` | `-..->` | `-...->` |

## Special characters that break syntax

It is possible to put text within quotes in order to render more troublesome characters. As in the example below:

##### Code:

mermaid

Ctrl + Enter|

### Entity codes to escape characters

It is possible to escape characters using the syntax exemplified here.

##### Code:

mermaid

Ctrl + Enter|

Numbers given are base 10, so `#` can be encoded as `#35;`. It is also supported to use HTML character names.

## Subgraphs

```
subgraph title
    graph definition
end
```

An example below:

##### Code:

mermaid

Ctrl + Enter|

You can also set an explicit id for the subgraph.

##### Code:

mermaid

Ctrl + Enter|

### flowcharts

With the graphtype flowchart it is also possible to set edges to and from subgraphs as in the flowchart below.

##### Code:

mermaid

Ctrl + Enter|

### Direction in subgraphs

With the graphtype flowcharts you can use the direction statement to set the direction which the subgraph will render like in this example.

##### Code:

mermaid

Ctrl + Enter|

#### Limitation

If any of a subgraph's nodes are linked to the outside, subgraph direction will be ignored. Instead the subgraph will inherit the direction of the parent graph:

##### Code:

mermaid

Ctrl + Enter|

## Markdown Strings

The "Markdown Strings" feature enhances flowcharts and mind maps by offering a more versatile string type, which supports text formatting options such as bold and italics, and automatically wraps text within labels.

##### Code:

mermaid

Ctrl + Enter|

Formatting:

* For bold text, use double asterisks (`**`) before and after the text.
* For italics, use single asterisks (`*`) before and after the text.
* With traditional strings, you needed to add `<br>` tags for text to wrap in nodes. However, markdown strings automatically wrap text when it becomes too long and allows you to start a new line by simply using a newline character instead of a `<br>` tag.

This feature is applicable to node labels, edge labels, and subgraph labels.

The auto wrapping can be disabled by using

```
---
config:
  markdownAutoWrap: false
---
graph LR
```

## Interaction

It is possible to bind a click event to a node, the click can lead to either a javascript callback or to a link which will be opened in a new browser tab.

INFO

This functionality is disabled when using `securityLevel='strict'` and enabled when using `securityLevel='loose'`.

```
click nodeId callback
click nodeId call callback()
```

* nodeId is the id of the node
* callback is the name of a javascript function defined on the page displaying the graph, the function will be called with the nodeId as parameter.

Examples of tooltip usage below:

html

```
<script>
  window.callback = function () {
    alert('A callback was triggered');
  };
</script>
```

The tooltip text is surrounded in double quotes. The styles of the tooltip are set by the class `.mermaidTooltip`.

##### Code:

mermaid

Ctrl + Enter|

> **Success** The tooltip functionality and the ability to link to urls are available from version 0.5.2.

?> Due to limitations with how Docsify handles JavaScript callback functions, an alternate working demo for the above code can be viewed at [this jsfiddle](https://jsfiddle.net/yk4h7qou/2/).

Links are opened in the same browser tab/window by default. It is possible to change this by adding a link target to the click definition (`_self`, `_blank`, `_parent` and `_top` are supported):

##### Code:

mermaid

Ctrl + Enter|

Beginner's tip—a full example using interactive links in a html context:

html

```
<body>
  <pre class="mermaid">
    flowchart LR
        A-->B
        B-->C
        C-->D
        click A callback "Tooltip"
        click B "https://www.github.com" "This is a link"
        click C call callback() "Tooltip"
        click D href "https://www.github.com" "This is a link"
  </pre>

  <script>
    window.callback = function () {
      alert('A callback was triggered');
    };
    const config = {
      startOnLoad: true,
      htmlLabels: true,
      flowchart: { useMaxWidth: true, curve: 'cardinal' },
      securityLevel: 'loose',
    };
    mermaid.initialize(config);
  </script>
</body>
```

### Comments

Comments can be entered within a flow diagram, which will be ignored by the parser. Comments need to be on their own line, and must be prefaced with `%%` (double percent signs). Any text after the start of the comment to the next newline will be treated as a comment, including any flow syntax

##### Code:

mermaid

Ctrl + Enter|

## Styling and classes

### Styling links

It is possible to style links. For instance, you might want to style a link that is going backwards in the flow. As links have no ids in the same way as nodes, some other way of deciding what style the links should be attached to is required. Instead of ids, the order number of when the link was defined in the graph is used, or use default to apply to all links. In the example below the style defined in the linkStyle statement will belong to the fourth link in the graph:

```
linkStyle 3 stroke:#ff3,stroke-width:4px,color:red;
```

It is also possible to add style to multiple links in a single statement, by separating link numbers with commas:

```
linkStyle 1,2,7 color:blue;
```

### Styling line curves

It is possible to style the type of curve used for lines between items, if the default method does not meet your needs. Available curve styles include `basis`, `bumpX`, `bumpY`, `cardinal`, `catmullRom`, `linear`, `monotoneX`, `monotoneY`, `natural`, `step`, `stepAfter`, and `stepBefore`.

For a full list of available curves, including an explanation of custom curves, refer to the [Shapes](https://d3js.org/d3-shape/curve) documentation in the [d3-shape](https://github.com/d3/d3-shape/) project.

Line styling can be achieved in two ways:

1. Change the curve style of all the lines
2. Change the curve style of a particular line

#### Diagram level curve style

In this example, a left-to-right graph uses the `stepBefore` curve style:

```
---
config:
  flowchart:
    curve: stepBefore
---
graph LR
```

#### Edge level curve style using Edge IDs (v11.10.0+)

You can assign IDs to [edges](#attaching-an-id-to-edges). After assigning an ID you can modify the line style by modifying the edge's `curve` property using the following syntax:

##### Code:

mermaid

Ctrl + Enter|

info

```
Any edge curve style modified at the edge level overrides the diagram level style.
```

info

```
If the same edge is modified multiple times the last modification will be rendered.
```

### Styling a node

It is possible to apply specific styles such as a thicker border or a different background color to a node.

##### Code:

mermaid

Ctrl + Enter|

#### Classes

More convenient than defining the style every time is to define a class of styles and attach this class to the nodes that should have a different look.

A class definition looks like the example below:

```
    classDef className fill:#f9f,stroke:#333,stroke-width:4px;
```

Also, it is possible to define style to multiple classes in one statement:

```
    classDef firstClassName,secondClassName font-size:12pt;
```

Attachment of a class to a node is done as per below:

```
    class nodeId1 className;
```

It is also possible to attach a class to a list of nodes in one statement:

```
    class nodeId1,nodeId2 className;
```

A shorter form of adding a class is to attach the classname to the node using the `:::`operator as per below:

##### Code:

mermaid

Ctrl + Enter|

This form can be used when declaring multiple links between nodes:

##### Code:

mermaid

Ctrl + Enter|

### CSS classes

It is also possible to predefine classes in CSS styles that can be applied from the graph definition as in the example below:

**Example style**

html

```
<style>
  .cssClass > rect {
    fill: #ff0000;
    stroke: #ffff00;
    stroke-width: 4px;
  }
</style>
```

**Example definition**

##### Code:

mermaid

Ctrl + Enter|

### Default class

If a class is named default it will be assigned to all classes without specific class definitions.

```
    classDef default fill:#f9f,stroke:#333,stroke-width:4px;
```

## Basic support for fontawesome

It is possible to add icons from fontawesome.

The icons are accessed via the syntax fa:#icon class name#.

##### Code:

mermaid

Ctrl + Enter|

There are two ways to display these FontAwesome icons:

### Register FontAwesome icon packs (v11.7.0+)

You can register your own FontAwesome icon pack following the ["Registering icon packs" instructions](./../config/icons.html).

Supported prefixes: `fa`, `fab`, `fas`, `far`, `fal`, `fad`.

INFO

Note that it will fall back to FontAwesome CSS if FontAwesome packs are not registered.

### Register FontAwesome CSS

Mermaid supports Font Awesome if the CSS is included on the website. Mermaid does not have any restriction on the version of Font Awesome that can be used.

Please refer the [Official Font Awesome Documentation](https://fontawesome.com/start) on how to include it in your website.

Adding this snippet in the `<head>` would add support for Font Awesome v6.5.1

html

```
<link
  href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"
  rel="stylesheet"
/>
```

### Custom icons

It is possible to use custom icons served from Font Awesome as long as the website imports the corresponding kit.

Note that this is currently a paid feature from Font Awesome.

For custom icons, you need to use the `fak` prefix.

**Example**

```
flowchart TD
    B[fa:fa-twitter] %% standard icon
    B-->E(fak:fa-custom-icon-name) %% custom icon
```

And trying to render it

##### Code:

mermaid

Ctrl + Enter|

## Graph declarations with spaces between vertices and link and without semicolon

* In graph declarations, the statements also can now end without a semicolon. After release 0.2.16, ending a graph statement with semicolon is just optional. So the below graph declaration is also valid along with the old declarations of the graph.
* A single space is allowed between vertices and the link. However there should not be any space between a vertex and its text and a link and its text. The old syntax of graph declaration will also work and hence this new feature is optional and is introduced to improve readability.

Below is the new declaration of the graph edges which is also valid along with the old declaration of the graph edges.

##### Code:

mermaid

Ctrl + Enter|

## Configuration

### Renderer

The layout of the diagram is done with the renderer. The default renderer is dagre.

Starting with Mermaid version 9.4, you can use an alternate renderer named elk. The elk renderer is better for larger and/or more complex diagrams.

The *elk* renderer is an experimental feature. You can change the renderer to elk by adding this directive:

```
config:
  flowchart:
    defaultRenderer: "elk"
```

INFO

Note that the site needs to use mermaid version 9.4+ for this to work and have this featured enabled in the lazy-loading configuration.

### Width

It is possible to adjust the width of the rendered flowchart.

This is done by defining **mermaid.flowchartConfig** or by the CLI to use a JSON file with the configuration. How to use the CLI is described in the mermaidCLI page. mermaid.flowchartConfig can be set to a JSON string with config parameters or the corresponding object.

javascript

```
mermaid.flowchartConfig = {
    width: 100%
}
```

---

## 2. Architecture Diagrams Documentation (v11.1.0+)

> In the context of mermaid-js, the architecture diagram is used to show the relationship between services and resources commonly found within the Cloud or CI/CD deployments. In an architecture diagram, services (nodes) are connected by edges. Related services can be placed within groups to better illustrate how they are organized.

## Example

##### Code:

mermaid

Ctrl + Enter|

## Syntax

The building blocks of an architecture are `groups`, `services`, `edges`, and `junctions`.

For supporting components, icons are declared by surrounding the icon name with `()`, while labels are declared by surrounding the text with `[]`.

To begin an architecture diagram, use the keyword `architecture-beta`, followed by your groups, services, edges, and junctions. While each of the 3 building blocks can be declared in any order, care must be taken to ensure the identifier was previously declared by another component.

### Groups

The syntax for declaring a group is:

```
group {group id}({icon name})[{title}] (in {parent id})?
```

Put together:

```
group public_api(cloud)[Public API]
```

creates a group identified as `public_api`, uses the icon `cloud`, and has the label `Public API`.

Additionally, groups can be placed within a group using the optional `in` keyword

```
group private_api(cloud)[Private API] in public_api
```

### Services

The syntax for declaring a service is:

```
service {service id}({icon name})[{title}] (in {parent id})?
```

Put together:

```
service database1(database)[My Database]
```

creates the service identified as `database1`, using the icon `database`, with the label `My Database`.

If the service belongs to a group, it can be placed inside it through the optional `in` keyword

```
service database1(database)[My Database] in private_api
```

### Edges

The syntax for declaring an edge is:

```
{serviceId}{{group}}?:{T|B|L|R} {<}?--{>}? {T|B|L|R}:{serviceId}{{group}}?
```

#### Edge Direction

The side of the service the edge comes out of is specified by adding a colon (`:`) to the side of the service connecting to the arrow and adding `L|R|T|B`

For example:

```
db:R -- L:server
```

creates an edge between the services `db` and `server`, with the edge coming out of the right of `db` and the left of `server`.

```
db:T -- L:server
```

creates a 90 degree edge between the services `db` and `server`, with the edge coming out of the top of `db` and the left of `server`.

#### Arrows

Arrows can be added to each side of an edge by adding `<` before the direction on the left, and/or `>` after the direction on the right.

For example:

```
subnet:R --> L:gateway
```

creates an edge with the arrow going into the `gateway` service

#### Edges out of Groups

To have an edge go from a group to another group or service within another group, the `{group}` modifier can be added after the `serviceId`.

For example:

```
service server[Server] in groupOne
service subnet[Subnet] in groupTwo

server{group}:B --> T:subnet{group}
```

creates an edge going out of `groupOne`, adjacent to `server`, and into `groupTwo`, adjacent to `subnet`.

It's important to note that `groupId`s cannot be used for specifying edges and the `{group}` modifier can only be used for services within a group.

### Junctions

Junctions are a special type of node which acts as a potential 4-way split between edges.

The syntax for declaring a junction is:

```
junction {junction id} (in {parent id})?
```

##### Code:

mermaid

Ctrl + Enter|

## Configuration

### `randomize` (v11.14.0+)

By default, architecture diagrams produce a deterministic layout: the same diagram source always renders with the same node positions. This is because the `randomize` option defaults to `false`.

Setting `randomize` to `true` randomizes initial node positions before running the layout algorithm, which may produce varied but potentially better-spaced layouts on each render.

Via frontmatter:

```
%%{init: {"architecture": {"randomize": true}}}%%
architecture-beta
    group api(cloud)[API]
    service db(database)[Database] in api
    service server(server)[Server] in api
    db:R --> L:server
```

Via `mermaid.initialize()`:

javascript

```
mermaid.initialize({
  architecture: {
    randomize: true,
  },
});
```

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `randomize` | boolean | `false` | Whether to randomize initial node positions before running the layout. |

## Icons

By default, architecture diagram supports the following icons: `cloud`, `database`, `disk`, `internet`, `server`. Users can use any of the 200,000+ icons available in iconify.design, or add other custom icons, by [registering an icon pack](./../config/icons.html).

After the icons are installed, they can be used in the architecture diagram by using the format "name:icon-name", where name is the value used when registering the icon pack.

##### Code:

mermaid

Ctrl + Enter|

---

## 3. C4 Diagrams

> C4 Diagram: This is an experimental diagram for now. The syntax and properties can change in future releases. Proper documentation will be provided when the syntax is stable.

Mermaid's C4 diagram syntax is compatible with plantUML. See example below:

##### Code:

mermaid

Ctrl + Enter|

For an example, see the source code demos/index.html

5 types of C4 charts are supported.

* System Context (C4Context)
* Container diagram (C4Container)
* Component diagram (C4Component)
* Dynamic diagram (C4Dynamic)
* Deployment diagram (C4Deployment)

Please refer to the linked document [C4-PlantUML syntax](https://github.com/plantuml-stdlib/C4-PlantUML/blob/master/README.md) for how to write the C4 diagram.

C4 diagram is fixed style, such as css color, so different css is not provided under different skins. updateElementStyle and UpdateElementStyle are written in the diagram last part. updateElementStyle is inconsistent with the original definition and updates the style of the relationship, including the offset of the text label relative to the original position.

The layout does not use a fully automated layout algorithm. The position of shapes is adjusted by changing the order in which statements are written. So there is no plan to support the following Layout statements. The number of shapes per row and the number of boundaries can be adjusted using UpdateLayoutConfig.

* Layout
  + Lay\_U, Lay\_Up
  + Lay\_D, Lay\_Down
  + Lay\_L, Lay\_Left
  + Lay\_R, Lay\_Right

The following unfinished features are not supported in the short term.

* [ ] sprite
* [ ] tags
* [ ] link
* [ ] Legend
* [x] System Context

  + [x] Person(alias, label, ?descr, ?sprite, ?tags, $link)
  + [x] Person\_Ext
  + [x] System(alias, label, ?descr, ?sprite, ?tags, $link)
  + [x] SystemDb
  + [x] SystemQueue
  + [x] System\_Ext
  + [x] SystemDb\_Ext
  + [x] SystemQueue\_Ext
  + [x] Boundary(alias, label, ?type, ?tags, $link)
  + [x] Enterprise\_Boundary(alias, label, ?tags, $link)
  + [x] System\_Boundary
* [x] Container diagram

  + [x] Container(alias, label, ?techn, ?descr, ?sprite, ?tags, $link)
  + [x] ContainerDb
  + [x] ContainerQueue
  + [x] Container\_Ext
  + [x] ContainerDb\_Ext
  + [x] ContainerQueue\_Ext
  + [x] Container\_Boundary(alias, label, ?tags, $link)
* [x] Component diagram

  + [x] Component(alias, label, ?techn, ?descr, ?sprite, ?tags, $link)
  + [x] ComponentDb
  + [x] ComponentQueue
  + [x] Component\_Ext
  + [x] ComponentDb\_Ext
  + [x] ComponentQueue\_Ext
* [x] Dynamic diagram

  + [x] RelIndex(index, from, to, label, ?tags, $link)
* [x] Deployment diagram

  + [x] Deployment\_Node(alias, label, ?type, ?descr, ?sprite, ?tags, $link)
  + [x] Node(alias, label, ?type, ?descr, ?sprite, ?tags, $link): short name of Deployment\_Node()
  + [x] Node\_L(alias, label, ?type, ?descr, ?sprite, ?tags, $link): left aligned Node()
  + [x] Node\_R(alias, label, ?type, ?descr, ?sprite, ?tags, $link): right aligned Node()
* [x] Relationship Types

  + [x] Rel(from, to, label, ?techn, ?descr, ?sprite, ?tags, $link)
  + [x] BiRel (bidirectional relationship)
  + [x] Rel\_U, Rel\_Up
  + [x] Rel\_D, Rel\_Down
  + [x] Rel\_L, Rel\_Left
  + [x] Rel\_R, Rel\_Right
  + [x] Rel\_Back
  + [x] RelIndex \* Compatible with C4-PlantUML syntax, but ignores the index parameter. The sequence number is determined by the order in which the rel statements are written.
* [ ] Custom tags/stereotypes support and skin param updates

  + [ ] AddElementTag(tagStereo, ?bgColor, ?fontColor, ?borderColor, ?shadowing, ?shape, ?sprite, ?techn, ?legendText, ?legendSprite): Introduces a new element tag. The styles of the tagged elements are updated and the tag is displayed in the calculated legend.
  + [ ] AddRelTag(tagStereo, ?textColor, ?lineColor, ?lineStyle, ?sprite, ?techn, ?legendText, ?legendSprite): Introduces a new Relationship tag. The styles of the tagged relationships are updated and the tag is displayed in the calculated legend.
  + [x] UpdateElementStyle(elementName, ?bgColor, ?fontColor, ?borderColor, ?shadowing, ?shape, ?sprite, ?techn, ?legendText, ?legendSprite): This call updates the default style of the elements (component, ...) and creates no additional legend entry.
  + [x] UpdateRelStyle(from, to, ?textColor, ?lineColor, ?offsetX, ?offsetY): This call updates the default relationship colors and creates no additional legend entry. Two new parameters, offsetX and offsetY, are added to set the offset of the original position of the text.
  + [ ] RoundedBoxShape(): This call returns the name of the rounded box shape and can be used as ?shape argument.
  + [ ] EightSidedShape(): This call returns the name of the eight sided shape and can be used as ?shape argument.
  + [ ] DashedLine(): This call returns the name of the dashed line and can be used as ?lineStyle argument.
  + [ ] DottedLine(): This call returns the name of the dotted line and can be used as ?lineStyle argument.
  + [ ] BoldLine(): This call returns the name of the bold line and can be used as ?lineStyle argument.
  + [x] UpdateLayoutConfig(?c4ShapeInRow, ?c4BoundaryInRow): New. This call updates the default c4ShapeInRow(4) and c4BoundaryInRow(2).

There are two ways to assign parameters with question marks. One uses the non-named parameter assignment method in the order of the parameters, and the other uses the named parameter assignment method, where the name must start with a $ symbol.

Example: UpdateRelStyle(from, to, ?textColor, ?lineColor, ?offsetX, ?offsetY)

```
UpdateRelStyle(customerA, bankA, "red", "blue", "-40", "60")
UpdateRelStyle(customerA, bankA, $offsetX="-40", $offsetY="60", $lineColor="blue", $textColor="red")
UpdateRelStyle(customerA, bankA, $offsetY="60")
```

## C4 System Context Diagram (C4Context)

##### Code:

mermaid

Ctrl + Enter|

## C4 Container diagram (C4Container)

##### Code:

mermaid

Ctrl + Enter|

## C4 Component diagram (C4Component)

##### Code:

mermaid

Ctrl + Enter|

## C4 Dynamic diagram (C4Dynamic)

##### Code:

mermaid

Ctrl + Enter|

## C4 Deployment diagram (C4Deployment)

##### Code:

mermaid

Ctrl + Enter|

---

## 4. Sequence diagrams

> A Sequence diagram is an interaction diagram that shows how processes operate with one another and in what order.

Mermaid can render sequence diagrams.

##### Code:

mermaid

Ctrl + Enter|

INFO

A note on nodes, the word "end" could potentially break the diagram, due to the way that the mermaid language is scripted.

If unavoidable, one must use parentheses(), quotation marks "", or brackets {},[], to enclose the word "end". i.e : (end), [end], {end}.

## Syntax

### Participants

The participants can be defined implicitly as in the first example on this page. The participants or actors are rendered in order of appearance in the diagram source text. Sometimes you might want to show the participants in a different order than how they appear in the first message. It is possible to specify the actor's order of appearance by doing the following:

##### Code:

mermaid

Ctrl + Enter|

### Actors

If you specifically want to use the actor symbol instead of a rectangle with text you can do so by using actor statements as per below.

##### Code:

mermaid

Ctrl + Enter|

### Boundary

If you want to use the boundary symbol for a participant, use the JSON configuration syntax as shown below.

##### Code:

mermaid

Ctrl + Enter|

### Control

If you want to use the control symbol for a participant, use the JSON configuration syntax as shown below.

##### Code:

mermaid

Ctrl + Enter|

### Entity

If you want to use the entity symbol for a participant, use the JSON configuration syntax as shown below.

##### Code:

mermaid

Ctrl + Enter|

### Database

If you want to use the database symbol for a participant, use the JSON configuration syntax as shown below.

##### Code:

mermaid

Ctrl + Enter|

### Collections

If you want to use the collections symbol for a participant, use the JSON configuration syntax as shown below.

##### Code:

mermaid

Ctrl + Enter|

### Queue

If you want to use the queue symbol for a participant, use the JSON configuration syntax as shown below.

##### Code:

mermaid

Ctrl + Enter|

### Aliases

The actor can have a convenient identifier and a descriptive label. Aliases can be defined in two ways: using external syntax with the `as` keyword, or inline within the configuration object.

#### External Alias Syntax

You can define an alias using the `as` keyword after the participant declaration:

##### Code:

mermaid

Ctrl + Enter|

The external alias syntax also works with participant stereotype configurations, allowing you to combine type specification with aliases:

##### Code:

mermaid

Ctrl + Enter|

#### Inline Alias Syntax

Alternatively, you can define an alias directly inside the configuration object using the `"alias"` field. This works with both `participant` and `actor` keywords:

##### Code:

mermaid

Ctrl + Enter|

#### Alias Precedence

When both inline alias (in the configuration object) and external alias (using `as` keyword) are provided, the **external alias takes precedence**:

##### Code:

mermaid

Ctrl + Enter|

In the example above, "External Name" and "External DB" will be displayed, not "Internal Name" and "Internal DB".

### Actor Creation and Destruction (v10.3.0+)

It is possible to create and destroy actors by messages. To do so, add a create or destroy directive before the message.

```
create participant B
A --> B: Hello
```

Create directives support actor/participant distinction and aliases. The sender or the recipient of a message can be destroyed but only the recipient can be created.

##### Code:

mermaid

Ctrl + Enter|

#### Unfixable actor/participant creation/deletion error

If an error of the following type occurs when creating or deleting an actor/participant:

> The destroyed participant **participant-name** does not have an associated destroying message after its declaration. Please check the sequence diagram.

And fixing diagram code does not get rid of this error and rendering of all other diagrams results in the same error, then you need to update the mermaid version to (v10.7.0+).

### Grouping / Box

The actor(s) can be grouped in vertical boxes. You can define a color (if not, it will be transparent) and/or a descriptive label using the following notation:

```
box Aqua Group Description
... actors ...
end
box Group without description
... actors ...
end
box rgb(33,66,99)
... actors ...
end
box rgba(33,66,99,0.5)
... actors ...
end
```

INFO

If your group name is a color you can force the color to be transparent:

```
box transparent Aqua
... actors ...
end
```

##### Code:

mermaid

Ctrl + Enter|

## Messages

Messages can be of two displayed either solid or with a dotted line.

```
[Actor][Arrow][Actor]:Message text
```

Lines can be solid or dotted, and can end with various types of arrowheads, crosses, or open arrows.

#### Supported Arrow Types

**Standard Arrow Types**

| Type | Description |
| --- | --- |
| `->` | Solid line without arrow |
| `-->` | Dotted line without arrow |
| `->>` | Solid line with arrowhead |
| `-->>` | Dotted line with arrowhead |
| `<<->>` | Solid line with bidirectional arrowheads (v11.0.0+) |
| `<<-->>` | Dotted line with bidirectional arrowheads (v11.0.0+) |
| `-x` | Solid line with a cross at the end |
| `--x` | Dotted line with a cross at the end |
| `-)` | Solid line with an open arrow at the end (async) |
| `--)` | Dotted line with a open arrow at the end (async) |

**Half-Arrows (v11.12.3+)**

The following half-arrow types are supported for more expressive sequence diagrams. Both solid and dotted variants are available by increasing the number of dashes (`-` → `--`).

---

| Type | Description |
| --- | --- |
| `-|\` | Solid line with top half arrowhead |
| `--|\` | Dotted line with top half arrowhead |
| `-|/` | Solid line with bottom half arrowhead |
| `--|/` | Dotted line with bottom half arrowhead |
| `/|-` | Solid line with reverse top half arrowhead |
| `/|--` | Dotted line with reverse top half arrowhead |
| `\\-` | Solid line with reverse bottom half arrowhead |
| `\\--` | Dotted line with reverse bottom half arrowhead |
| `-\\` | Solid line with top stick half arrowhead |
| `--\\` | Dotted line with top stick half arrowhead |
| `-//` | Solid line with bottom stick half arrowhead |
| `--//` | Dotted line with bottom stick half arrowhead |
| `//-` | Solid line with reverse top stick half arrowhead |
| `//--` | Dotted line with reverse top stick half arrowhead |
| `\\-` | Solid line with reverse bottom stick half arrowhead |
| `\\--` | Dotted line with reverse bottom stick half arrowhead |

## Central Connections (v11.12.3+)

Mermaid sequence diagrams support **central lifeline connections** using a `()`. This is useful to represent messages or signals that connect to a central point, rather than from one actor directly to another.

To indicate a central connection, append `()` to the arrow syntax.

#### Basic Syntax

##### Code:

mermaid

Ctrl + Enter|

## Activations

It is possible to activate and deactivate an actor. (de)activation can be dedicated declarations:

##### Code:

mermaid

Ctrl + Enter|

There is also a shortcut notation by appending `+`/`-` suffix to the message arrow:

##### Code:

mermaid

Ctrl + Enter|

Activations can be stacked for same actor:

##### Code:

mermaid

Ctrl + Enter|

## Notes

It is possible to add notes to a sequence diagram. This is done by the notation Note [ right of | left of | over ] [Actor]: Text in note content

See the example below:

##### Code:

mermaid

Ctrl + Enter|

It is also possible to create notes spanning two participants:

##### Code:

mermaid

Ctrl + Enter|

## Line breaks

Line break can be added to Note and Message:

##### Code:

mermaid

Ctrl + Enter|

Line breaks in Actor names requires aliases:

##### Code:

mermaid

Ctrl + Enter|

## Loops

It is possible to express loops in a sequence diagram. This is done by the notation

```
loop Loop text
... statements ...
end
```

See the example below:

##### Code:

mermaid

Ctrl + Enter|

## Alt

It is possible to express alternative paths in a sequence diagram. This is done by the notation

```
alt Describing text
... statements ...
else
... statements ...
end
```

or if there is sequence that is optional (if without else).

```
opt Describing text
... statements ...
end
```

See the example below:

##### Code:

mermaid

Ctrl + Enter|

## Parallel

It is possible to show actions that are happening in parallel.

This is done by the notation

```
par [Action 1]
... statements ...
and [Action 2]
... statements ...
and [Action N]
... statements ...
end
```

See the example below:

##### Code:

mermaid

Ctrl + Enter|

It is also possible to nest parallel blocks.

##### Code:

mermaid

Ctrl + Enter|

## Critical Region

It is possible to show actions that must happen automatically with conditional handling of circumstances.

This is done by the notation

```
critical [Action that must be performed]
... statements ...
option [Circumstance A]
... statements ...
option [Circumstance B]
... statements ...
end
```

See the example below:

##### Code:

mermaid

Ctrl + Enter|

It is also possible to have no options at all

##### Code:

mermaid

Ctrl + Enter|

This critical block can also be nested, equivalently to the `par` statement as seen above.

## Break

It is possible to indicate a stop of the sequence within the flow (usually used to model exceptions).

This is done by the notation

```
break [something happened]
... statements ...
end
```

See the example below:

##### Code:

mermaid

Ctrl + Enter|

## Background Highlighting

It is possible to highlight flows by providing colored background rects. This is done by the notation

```
rect COLOR
... content ...
end
```

The colors are defined using rgb and rgba syntax.

```
rect rgb(0, 255, 0)
... content ...
end
```

```
rect rgba(0, 0, 255, .1)
... content ...
end
```

See the examples below:

##### Code:

mermaid

Ctrl + Enter|

## Comments

Comments can be entered within a sequence diagram, which will be ignored by the parser. Comments need to be on their own line, and must be prefaced with `%%` (double percent signs). Any text after the start of the comment to the next newline will be treated as a comment, including any diagram syntax

##### Code:

mermaid

Ctrl + Enter|

## Entity codes to escape characters

It is possible to escape characters using the syntax exemplified here.

##### Code:

mermaid

Ctrl + Enter|

Numbers given are base 10, so `#` can be encoded as `#35;`. It is also supported to use HTML character names.

Because semicolons can be used instead of line breaks to define the markup, you need to use `#59;` to include a semicolon in message text.

## sequenceNumbers

It is possible to get a sequence number attached to each arrow in a sequence diagram. This can be configured when adding mermaid to the website as shown below:

html

```
<script>
  mermaid.initialize({ sequence: { showSequenceNumbers: true } });
</script>
```

It can also be turned on via the diagram code as in the diagram:

##### Code:

mermaid

Ctrl + Enter|

## Actor Menus

Actors can have popup-menus containing individualized links to external pages. For example, if an actor represented a web service, useful links might include a link to the service health dashboard, repo containing the code for the service, or a wiki page describing the service.

This can be configured by adding one or more link lines with the format:

```
link <actor>: <link-label> @ <link-url>
```

##### Code:

mermaid

Ctrl + Enter|

#### Advanced Menu Syntax

There is an advanced syntax that relies on JSON formatting. If you are comfortable with JSON format, then this exists as well.

This can be configured by adding the links lines with the format:

```
links <actor>: <json-formatted link-name link-url pairs>
```

An example is below:

##### Code:

mermaid

Ctrl + Enter|

## Styling

Styling of a sequence diagram is done by defining a number of css classes. During rendering these classes are extracted from the file located at src/themes/sequence.scss

### Classes used

| Class | Description |
| --- | --- |
| actor | Styles for the actor box. |
| actor-top | Styles for the actor figure/ box at the top of the diagram. |
| actor-bottom | Styles for the actor figure/ box at the bottom of the diagram. |
| text.actor | Styles for text of all of the actors. |
| text.actor-box | Styles for text of the actor box. |
| text.actor-man | Styles for text of the actor figure. |
| actor-line | The vertical line for an actor. |
| messageLine0 | Styles for the solid message line. |
| messageLine1 | Styles for the dotted message line. |
| messageText | Defines styles for the text on the message arrows. |
| labelBox | Defines styles label to left in a loop. |
| labelText | Styles for the text in label for loops. |
| loopText | Styles for the text in the loop box. |
| loopLine | Defines styles for the lines in the loop box. |
| note | Styles for the note box. |
| noteText | Styles for the text on in the note boxes. |

### Sample stylesheet

css

```
body {
  background: white;
}

.actor {
  stroke: #ccccff;
  fill: #ececff;
}
text.actor {
  fill: black;
  stroke: none;
  font-family: Helvetica;
}

.actor-line {
  stroke: grey;
}

.messageLine0 {
  stroke-width: 1.5;
  stroke-dasharray: '2 2';
  marker-end: 'url(#arrowhead)';
  stroke: black;
}

.messageLine1 {
  stroke-width: 1.5;
  stroke-dasharray: '2 2';
  stroke: black;
}

#arrowhead {
  fill: black;
}

.messageText {
  fill: black;
  stroke: none;
  font-family: 'trebuchet ms', verdana, arial;
  font-size: 14px;
}

.labelBox {
  stroke: #ccccff;
  fill: #ececff;
}

.labelText {
  fill: black;
  stroke: none;
  font-family: 'trebuchet ms', verdana, arial;
}

.loopText {
  fill: black;
  stroke: none;
  font-family: 'trebuchet ms', verdana, arial;
}

.loopLine {
  stroke-width: 2;
  stroke-dasharray: '2 2';
  marker-end: 'url(#arrowhead)';
  stroke: #ccccff;
}

.note {
  stroke: #decc93;
  fill: #fff5ad;
}

.noteText {
  fill: black;
  stroke: none;
  font-family: 'trebuchet ms', verdana, arial;
  font-size: 14px;
}
```

## Configuration

It is possible to adjust the margins for rendering the sequence diagram.

This is done by defining `mermaid.sequenceConfig` or by the CLI to use a json file with the configuration. How to use the CLI is described in the [mermaidCLI](./../config/mermaidCLI.html) page. `mermaid.sequenceConfig` can be set to a JSON string with config parameters or the corresponding object.

javascript

```
mermaid.sequenceConfig = {
  diagramMarginX: 50,
  diagramMarginY: 10,
  boxTextMargin: 5,
  noteMargin: 10,
  messageMargin: 35,
  mirrorActors: true,
};
```

### Possible configuration parameters:

| Parameter | Description | Default value |
| --- | --- | --- |
| mirrorActors | Turns on/off the rendering of actors below the diagram as well as above it | false |
| bottomMarginAdj | Adjusts how far down the graph ended. Wide borders styles with css could generate unwanted clipping which is why this config param exists. | 1 |
| actorFontSize | Sets the font size for the actor's description | 14 |
| actorFontFamily | Sets the font family for the actor's description | "Open Sans", sans-serif |
| actorFontWeight | Sets the font weight for the actor's description | "Open Sans", sans-serif |
| noteFontSize | Sets the font size for actor-attached notes | 14 |
| noteFontFamily | Sets the font family for actor-attached notes | "trebuchet ms", verdana, arial |
| noteFontWeight | Sets the font weight for actor-attached notes | "trebuchet ms", verdana, arial |
| noteAlign | Sets the text alignment for text in actor-attached notes | center |
| messageFontSize | Sets the font size for actor<->actor messages | 16 |
| messageFontFamily | Sets the font family for actor<->actor messages | "trebuchet ms", verdana, arial |
| messageFontWeight | Sets the font weight for actor<->actor messages | "trebuchet ms", verdana, arial |

---

## Bibliography

1. [Flowcharts - Basic Syntax](https://mermaid.js.org/syntax/flowchart.html)
2. [Architecture Diagrams Documentation (v11.1.0+)](https://mermaid.js.org/syntax/architecture.html)
3. [C4 Diagrams](https://mermaid.js.org/syntax/c4.html)
4. [Sequence diagrams](https://mermaid.js.org/syntax/sequenceDiagram.html)