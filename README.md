# Designing-Parser-with-Python
Implementation of Parser with python

## Execution
Input from terminal use (hit double enter to terminate),
```
$ python3 main.py
```

To Run the tests provided in directory use the -t flag (add -p flag for print)
```
$ python3 main.py -t
```

To run a file containing code,
```
$ python3 main.py -p file_name
```

## Example
![image](https://user-images.githubusercontent.com/124317396/229978763-e14e2c62-52b9-4b9a-b7b0-00149b669579.png)

The parse output is:
```
{
  "type": "Program",
  "body": [
    {
      "type": "ForStatement",
      "init": {
        "type": "VariableStatement",
        "declarations": [
          {
            "type": "VariableDeclaration",
            "id": {
              "type": "Identifer",
              "name": "i"
            },
            "init": {
              "type": "NumericLiteral",
              "value": 0
            }
          },
          {
            "type": "VariableDeclaration",
            "id": {
              "type": "Identifer",
              "name": "j"
            },
            "init": {
              "type": "NumericLiteral",
              "value": 0
            }
          }
        ]
      },
      "test": {
        "type": "BinaryExpression",
        "operator": "<",
        "left": {
          "type": "Identifer",
          "name": "i"
        },
        "right": {
          "type": "NumericLiteral",
          "value": 9
        }
      },
      "update": {
        "type": "AssignmentExpression",
        "operator": "+=",
        "left": {
          "type": "Identifer",
          "name": "i"
        },
        "right": {
          "type": "Identifer",
          "name": "j"
        }
      },
      "body": {
        "type": "BlockStatement",
        "body": [
          {
            "type": "ExpressionStatement",
            "expression": {
              "type": "AssignmentExpression",
              "operator": "+=",
              "left": {
                "type": "Identifer",
                "name": "x"
              },
              "right": {
                "type": "Identifer",
                "name": "j"
              }
            }
          },
          {
            "type": "ExpressionStatement",
            "expression": {
              "type": "UnaryExpression",
              "operator": "+",
              "argument": {
                "type": "UnaryExpression",
                "operator": "+",
                "argument": {
                  "type": "Identifer",
                  "name": "j"
                }
              }
            }
          }
        ]
      }
    }
  ]
}
```
