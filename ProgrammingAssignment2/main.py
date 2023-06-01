from sympy import Symbol, inverse_laplace_transform, exp
from sympy.physics.control.control_plots import pole_zero_plot, bode_magnitude_plot, bode_phase_plot, bode_plot, step_response_plot
from sympy.physics.control.lti import TransferFunction

def process_fs(s_domain_func, s_var, limits):
    print(f"Processing function '{s_domain_func}'")
    print(f"Using '{s_var}' and the following limits:")
    print(limits)

    num, den = s_domain_func.as_numer_denom()     # Extract the numerator and denominator from the symbolic expression

    for variable, limit_values in limits.items():       # Substitute limit values into the numerator and denominator
        variable_symbol = Symbol(variable)
        if not isinstance(limit_values, tuple):    # Handle both single numeric value and one-item tuple
            limit_values = (limit_values,)
        elif len(limit_values) == 1:   # If only one value is given, use it for all three limits.
            limit_values = (limit_values[0], limit_values[0], limit_values[0]) # Handle different lengths of limit tuples
        elif len(limit_values) == 2:    # If only two values are given, use the second value for the third limit.
            limit_values = (limit_values[0], limit_values[1], limit_values[1])
        elif len(limit_values) == 3:    # If three values are given, use them as is.
            limit_values = (limit_values[0], limit_values[1], limit_values[2])
        
        for i, limit_value in enumerate(limit_values):
            num = num.subs(variable_symbol, limit_value)
            den = den.subs(variable_symbol, limit_value)


    tf = TransferFunction(num, den, s_var)     # Create the TransferFunction object
    print(f"list of Poles in this Transfer function: {tf.poles()}")
    print(f"list of Zeros in this Transfer function: {tf.zeros()}")
    bode_plot(tf)     # Generate the bode plot
    pole_zero_plot(tf)     # Generate the pole-zero plot

def test_func():
    s = Symbol("s")
    p1 = Symbol("p1")
    p2 = Symbol("p2")
    p3 = Symbol("p3")
    z1 = Symbol("z1")
    z2 = Symbol("z2")
    z3 = Symbol("z3")

    # sp = 1 / (s * p1) # low pass
    # sp = s / (s * p1 + 1) # high pass
    # sp = (s / (s * p1 + 1)) * (s * z1 + 1) # band pass
    # sp = (s * p1 + 1) / (s * z1 + 1) # band stop
    # sp = ((s * p1 + 1) / (s * z1 + 1)) * ((s * z1 + 1) / (s * p1 + 1)) # all pass
    # sp = (s + 1) / ((s - 2)*(s + 3)*(s**2 + 2*s + 5)) # random transfer function to test the code
    # sp = 100 / (s + 30) # A real pole 
    # sp = 100 * (s + 1) / (s**2 + 100 * s + 1000) # Real poles and zeros 
    # sp = 10 * (s + 10) / (s**2 + 3 * s) # pole at the origin 
    # sp = -100 * (s) / (s**3 + 12 * s**2 + 21 * s + 10) # repeated real poles, negative constant
    # sp = 3 * ((s + 10) / (s**2 + 3*s + 50)) # complex conj. poles
    # sp = 4 * ((s**2 + s + 25) / (s**3 + 100*s**2)) # multiple poles at origin, complex conj zeros
    # sp = (100 / (s + 30)) * exp(-0.01 * s) # time delay
    # sp = (s + 1) / ((s - 2)*(s + 3)*(s**2 + 2*s + 5))
    # sp = (2 + 42*s)/((1 + 2*s)*(1 + 40*s))

    # sp = (s + p1) / (s + p2)
    
    # sp = (s + 1) / ((s - 2)*(s + 3)*(s**2 + 2*s + 5))
    # sp = (2 + 42*s)/((1 + 2*s)*(1 + 40*s))
    
    # limits = {"p1": (1e3,)}
    # limits = {"p1": (1e3,), "z1": (1e2, 1e4)} # Second limit example 
    # limits = {"p1": 1e3, "p2": (10e3,)} # limit example to show limits dictionary work with either single numeric value or a one item tuple

    # limits = {"p1": 1e3}
    # limits = {"p1": (1e3, 1e4)}
    # limits = {"p1": (1e3, 5e3, 1e4)}

    # sp = s
    # limits = {"p1": 1}
    # sp = (s + z1) / (s + p1)
    # limits = {"p1": (1e3,), "z1": (1e2,)}
    # sp = ((s + z1)*(s + z2)) / ((s + p1)*(s + p2))
    # limits = {"p1": (1e3,), "p2": (10e3,), "z1": (1e2, 1e4), "z2": (1e3, 1e5)}
    sp = ((s + z1)*(s + z2)*(s + z3)) / ((s + p1)*(s + p2)*(s + p3))
    limits = {"p1": (1e3,), "p2": (10e3,), "p3": (100e3,), "z1": (1e2, 1e4), "z2": (1e3, 1e5), "z3": (1e4, 1e6)}
    
    process_fs(sp, s, limits)

if __name__ == "__main__":
    test_func()