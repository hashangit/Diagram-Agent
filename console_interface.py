import colorama
from colorama import Fore, Back, Style
import os

colorama.init(autoreset=True)

class ConsoleInterface:
    def __init__(self):
        try:
            self.width = os.get_terminal_size().columns
        except OSError:
            self.width = 80  # Default width if terminal size can't be determined

    def _print_header(self, text, emoji="📊"):
        print("\n" + Fore.CYAN + Style.BRIGHT + "=" * self.width)
        print(Fore.CYAN + Style.BRIGHT + f"{emoji}  {text}  {emoji}".center(self.width))
        print(Fore.CYAN + Style.BRIGHT + "=" * self.width + "\n")

    def _print_subheader(self, text, emoji="🔹"):
        print("\n" + Fore.YELLOW + Style.BRIGHT + "-" * self.width)
        print(Fore.YELLOW + Style.BRIGHT + f"{emoji}  {text}  {emoji}".center(self.width))
        print(Fore.YELLOW + Style.BRIGHT + "-" * self.width + "\n")

    def get_user_input(self, prompt: str) -> str:
        return input(Fore.GREEN + Style.BRIGHT + f"➤ {prompt}" + Style.RESET_ALL)

    def display_message(self, message: str):
        print(Fore.WHITE + f"ℹ️  {message}")

    def display_results(self, brief: str, mermaid_code: str):
        self._print_header("Diagramming Results", "🎉")
        
        self._print_subheader("Expert Brief Summary", "📝")
        print(Fore.WHITE + brief)
        print()

        self._print_subheader("Generated Mermaid Code", "💻")
        print(Fore.MAGENTA + Style.BRIGHT + "```mermaid")
        print(Fore.WHITE + mermaid_code)
        print(Fore.MAGENTA + Style.BRIGHT + "```")

    def ask_for_clarification(self, ai_response: str) -> str:
        self._print_subheader("Clarification Needed", "❓")
        print(Fore.RED + "Your answer seems incomplete. Here's some feedback:")
        print(Fore.WHITE + ai_response)
        return self.get_user_input("Can you please provide more information? ")

    def display_welcome_message(self):
        self._print_header("Welcome to the Mermaid Diagram Generator", "👋")
        print(Fore.WHITE + "This interactive tool will guide you through creating a Mermaid diagram.")
        print(Fore.WHITE + "Please follow these steps:")
        print(Fore.CYAN + "1. Answer the questions about your diagram")
        print(Fore.CYAN + "2. Review the generated Mermaid code")
        print(Fore.CYAN + "3. Use the code in your preferred Mermaid renderer")
        print()

    def display_question(self, question: str):
        self._print_subheader("Question", "❔")
        print(Fore.BLUE + Style.BRIGHT + question)

    def display_completion_message(self):
        self._print_header("Diagram Generation Complete", "🎈")
        print(Fore.GREEN + Style.BRIGHT + "🌟 Your Mermaid diagram has been successfully generated! 🌟")
        print(Fore.WHITE + "Next steps:")
        print(Fore.CYAN + "1. Copy the generated Mermaid code")
        print(Fore.CYAN + "2. Paste it into your preferred Mermaid renderer")
        print(Fore.CYAN + "3. Visualize and enjoy your diagram!")
        print()

    def display_unsupported_diagram_message(self, error_message: str):
        self._print_header("Unsupported Diagram Type", "⚠️")
        print(Fore.RED + Style.BRIGHT + error_message)
        print(Fore.WHITE + "Please try again with one of these supported Mermaid diagram types:")
        print(Fore.CYAN + "• Flowchart")
        print(Fore.CYAN + "• Sequence Diagram")
        print(Fore.CYAN + "• Class Diagram")
        print(Fore.CYAN + "• State Diagram")
        print(Fore.CYAN + "• Entity Relationship Diagram")
        print(Fore.CYAN + "• User Journey")
        print(Fore.CYAN + "• Gantt Chart")
        print(Fore.CYAN + "• Pie Chart")
        print()

# Example usage
if __name__ == "__main__":
    interface = ConsoleInterface()
    interface.display_welcome_message()
    interface.display_question("What type of diagram would you like to create?")
    response = interface.get_user_input("Your answer: ")
    interface.display_message("You selected: " + response)
    interface.display_results("This is a brief summary of the diagram.", "graph TD;\nA-->B;\nB-->C;\nC-->D;\nD-->E;")
    interface.display_completion_message()