from sympy import Symbol
from sympy.physics.control.control_plots import pole_zero_plot, bode_magnitude_plot, bode_phase_plot, bode_plot, step_response_plot
from sympy.physics.control.lti import TransferFunction

def process_fs(s_domain_func, s_var, limits):
    print(f"Processing function '{s_domain_func}'")
    print(f"Using '{s_var}' and the following limits:")
    print(limits)

    num, den = s_domain_func.as_numer_denom()     # Extract the numerator and denominator from the symbolic expression
    tf = TransferFunction(num, den, s_var)     # Create the TransferFunction object
    bode_plot(tf)     # Generate the bode plot
    pole_zero_plot(tf)     # Generate the pole-zero plot

def test_func():
    s = Symbol("s")
    p1 = Symbol("p1")
    # sp = 1 / (s * p1)
    # sp = (s + 1) / ((s - 2)*(s + 3)*(s**2 + 2*s + 5))
    sp = (2 + 42*s)/((1 + 2*s)*(1 + 40*s))
    limits = {"p1": (1e3,)}
    process_fs(sp, s, limits)

if __name__ == "__main__":
    test_func()