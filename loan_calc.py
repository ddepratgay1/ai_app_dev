python
def calculate_loan_payment(interest_rate_annual, term_years, present_value):
    """
    Calculates the monthly loan payment.

    Args:
        interest_rate_annual (float): The annual interest rate as a decimal (e.g., 0.05 for 5%).
        term_years (int): The loan term in years.
        present_value (float): The principal loan amount (the present value).

    Returns:
        float: The monthly loan payment amount.
    """
    if term_years <= 0:
        raise ValueError("Loan term must be greater than zero years.")
    if present_value <= 0:
        raise ValueError("Present value (principal) must be greater than zero.")

    # Convert annual interest rate to a monthly rate
    monthly_interest_rate = interest_rate_annual / 12

    # Calculate total number of payments (months)
    number_of_payments = term_years * 12

    if monthly_interest_rate == 0:
        # If the interest rate is zero, the payment is simply the principal
        # divided by the total number of payments.
        return present_value / number_of_payments
    else:
        # Standard loan payment formula (PMT)
        # PMT = P * [ i(1 + i)^n ] / [ (1 + i)^n – 1]
        # where:
        # P = Present Value (principal loan amount)
        # i = Monthly interest rate
        # n = Total number of payments
        
        numerator = present_value * monthly_interest_rate * (1 + monthly_interest_rate)**number_of_payments
        denominator = (1 + monthly_interest_rate)**number_of_payments - 1

        if denominator == 0:
            # This case should ideally not be reached with a non-zero monthly_interest_rate
            # and a valid number_of_payments, but good to handle for robustness.
            return float('inf') # Or raise a more specific error
        
        return numerator / denominator