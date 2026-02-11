"""
Session 7: Class Structure, Encapsulation, and Abstraction.

This module provides a class to validate user-submitted text against
length and security requirements.
"""

import string


class InputValidator:
    """
    A class used to represent an input validation engine.

    Attributes:
        text (str): The sanitized (stripped) version of the input text.
    """

    def __init__(self, text):
        """
        Initializes the validator and performs basic encapsulation.

        Args:
            text (str): The raw string to be validated.
        """
        # Store the stripped version of 'text' in self.text
        self.text = text.strip()

    def is_long_enough(self, min_chars=20):
        """
        Internal logic to verify the length of the string.

        Args:
            min_chars (int): The threshold for a valid string. Defaults to 20.

        Returns:
            bool: True if length is >= min_chars, False otherwise.
        """
        return len(self.text) >= min_chars

    def is_safe(self):
        """
        Internal logic to check for dangerous SQL keywords and punctuation.

        Security Criteria:
        1. No SQL keywords: SELECT, DELETE, INSERT, UPDATE, DROP, --, ;
        2. No characters from string.punctuation.

        Returns:
            bool: True if no dangerous elements are found, False otherwise.
        """
        text_upper = self.text.upper()

        # Check for dangerous SQL keywords / patterns
        dangerous_keywords = ["SELECT", "DELETE", "INSERT", "UPDATE", "DROP", "--", ";"]
        for keyword in dangerous_keywords:
            if keyword in text_upper:
                return False

        # Check for any punctuation
        for char in self.text:
            if char in string.punctuation:
                return False

        return True

    def validate_all(self):
        """
        The Public Interface: Abstracts the internal validation logic.

        This method coordinates the execution of is_long_enough and is_safe.

        Returns:
            tuple: (bool, str)
                   - The bool indicates success/failure.
                   - The str provides the specific success or error message.
        """
        if not self.is_long_enough():
            return (False, "Text must be at least 20 characters.")

        if not self.is_safe():
            return (False, "Text contains unsafe content.")

        return (True, "Text is valid.")


if __name__ == "__main__":
    # Simple tests
    tests = [
        "too short",
        "This is long enough but has a semicolon;",
        "This is long enough and safe text",
        "DROP TABLE users",  # should fail
        "This is long enough but has punctuation!"  # should fail because of !
    ]

    for t in tests:
        validator = InputValidator(t)
        result = validator.validate_all()
        print(f"Input: {t!r}\nResult: {result}\n")
