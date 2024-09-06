# Mermaid Diagram Examples

# 1. Flowchart Example
flowchart = '''
flowchart TD
    A[Start] --> B{Is it?}
    B -->|Yes| C[OK]
    C --> D[Rethink]
    D --> B
    B ---->|No| E[End]
'''

# 2. Sequence Diagram Example
sequence = '''
sequenceDiagram
    participant Alice
    participant Bob
    Alice->>John: Hello John, how are you?
    loop Healthcheck
        John->>John: Fight against hypochondria
    end
    Note right of John: Rational thoughts <br/>prevail!
    John-->>Alice: Great!
    John->>Bob: How about you?
    Bob-->>John: Jolly good!
'''

# 3. Class Diagram Example
class_diagram = '''
classDiagram
    Animal <|-- Duck
    Animal <|-- Fish
    Animal <|-- Zebra
    Animal : +int age
    Animal : +String gender
    Animal: +isMammal()
    Animal: +mate()
    class Duck{
        +String beakColor
        +swim()
        +quack()
    }
    class Fish{
        -int sizeInFeet
        -canEat()
    }
    class Zebra{
        +bool is_wild
        +run()
    }
'''

# 4. Entity Relationship Diagram Example
er_diagram = '''
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE-ITEM : contains
    CUSTOMER }|..|{ DELIVERY-ADDRESS : uses
'''

# 5. Gantt Chart Example
gantt = '''
gantt
    title A Gantt Diagram
    dateFormat  YYYY-MM-DD
    section Section
    A task           :a1, 2014-01-01, 30d
    Another task     :after a1  , 20d
    section Another
    Task in sec      :2014-01-12  , 12d
    another task      : 24d
'''

# 6. Pie Chart Example
pie = '''
pie title Fruits in Pie Chart
    "Apples" : 40
    "Bananas" : 30
    "Cherries" : 20
    "Dates" : 10
'''

# Print all examples
print("Flowchart Example:")
print(flowchart)
print("\nSequence Diagram Example:")
print(sequence)
print("\nClass Diagram Example:")
print(class_diagram)
print("\nEntity Relationship Diagram Example:")
print(er_diagram)
print("\nGantt Chart Example:")
print(gantt)
print("\nPie Chart Example:")
print(pie)