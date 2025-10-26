"""Tool definitions for LLM simulations."""
from typing import List, Dict, Any, Optional, Callable
import json


class ToolRegistry:
    """Registry for tools that personas can use during simulations."""
    
    def __init__(self):
        """Initialize the tool registry."""
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.functions: Dict[str, Callable] = {}
        
    def register_tool(self, name: str, function: Callable, description: str, 
                     parameters: Dict[str, Any]):
        """
        Register a tool for use in simulations.
        
        Args:
            name: Tool function name
            function: Python function to execute
            description: Description for the LLM
            parameters: JSON schema for parameters
        """
        self.tools[name] = {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters
            }
        }
        self.functions[name] = function
    
    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Get all tool definitions for API calls."""
        return list(self.tools.values())
    
    def execute_tool(self, name: str, arguments: Dict[str, Any]) -> str:
        """
        Execute a tool by name with given arguments.
        
        Args:
            name: Tool name
            arguments: Tool arguments
            
        Returns:
            JSON string result
        """
        if name not in self.functions:
            return json.dumps({"error": f"Tool {name} not found"})
        
        try:
            result = self.functions[name](**arguments)
            return json.dumps({"status": "success", "result": result})
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})


# Example tools

def search_information(query: str, domain: Optional[str] = None) -> str:
    """
    Simulate searching for information.
    
    Args:
        query: Search query
        domain: Optional domain to search within
        
    Returns:
        Simulated search result
    """
    # In a real implementation, this could call an actual search API
    return f"Search results for '{query}'" + (f" in domain '{domain}'" if domain else "")


def calculate(expression: str) -> float:
    """
    Safely evaluate a mathematical expression.
    
    Args:
        expression: Mathematical expression to evaluate
        
    Returns:
        Calculation result
    """
    try:
        # Safe evaluation of math expressions
        # Note: In production, use a proper math parser
        allowed_names = {"abs": abs, "round": round, "min": min, "max": max}
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return float(result)
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")


def get_default_tool_registry() -> ToolRegistry:
    """
    Create a registry with default tools.
    
    Returns:
        ToolRegistry with default tools registered
    """
    registry = ToolRegistry()
    
    # Register search tool
    registry.register_tool(
        name="search_information",
        function=search_information,
        description="Search for information on a topic. Use this when you need factual information.",
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                },
                "domain": {
                    "type": "string",
                    "description": "Optional domain to search within (e.g., 'health', 'technology')"
                }
            },
            "required": ["query"]
        }
    )
    
    # Register calculator tool
    registry.register_tool(
        name="calculate",
        function=calculate,
        description="Perform mathematical calculations. Use this for any numerical computations.",
        parameters={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate (e.g., '2 + 2', '100 * 0.15')"
                }
            },
            "required": ["expression"]
        }
    )
    
    return registry

