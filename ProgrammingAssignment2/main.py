from sympy import Symbol, inverse_laplace_transform, exp, Heaviside, symbols
from sympy.physics.control.control_plots import pole_zero_plot, bode_magnitude_plot, bode_phase_plot, bode_plot, step_response_plot
from sympy.physics.control.lti import TransferFunction
import itertools

def process_fs(s_domain_func, s_var, limits):
    print(f"Processing function '{s_domain_func}'")
    print(f"Using '{s_var}' and the following limits:")
    print(limits)

    # for variable, limit_values in limits.items():       # Substitute limit values into the numerator and denominator
    #     variable_symbol = Symbol(variable)
    #     if not isinstance(limit_values, tuple):    # Handle both single numeric value and one-item tuple
    #         limit_values = (limit_values,)
    #     elif len(limit_values) == 1:   # If only one value is given, use it for all three limits.
    #         limit_values = (limit_values[0], limit_values[0], limit_values[0]) # Handle different lengths of limit tuples
    #     elif len(limit_values) == 2:    # If only two values are given, use the second value for the third limit.
    #         limit_values = (limit_values[0], limit_values[1], limit_values[1])
    #     elif len(limit_values) == 3:    # If three values are given, use them as is.
    #         limit_values = (limit_values[0], limit_values[1], limit_values[2])

    s_var = s_var
    num, den = s_domain_func.as_numer_denom()     # Extract the numerator and denominator from the symbolic expression
        
    symbols = s_domain_func.free_symbols
    symbol_keys = []

   # Extract keys from limits dictionary that match the symbols used in the transfer function
    for symbol in symbols:
        for key, value in limits.items():
            if str(symbol) == key:
                symbol_keys.append(key)
                break

    # Check if all symbols in the expression (except 's') have corresponding keys in the limits dictionary
    missing_symbols = [str(symbol) for symbol in symbols if str(symbol) not in symbol_keys and str(symbol) != str(s_var)]
    if missing_symbols:
        raise ValueError(f"ARE YOU SURE YOU INCLUDED THE VARIABLE {missing_symbols} FROM TRANSFER FUNCTION IN THE LIMITS DICTIONARY?")

    # Generate combinations of symbol values
    symbol_limits = []
    for key in symbol_keys:
        value = limits[key]
        if isinstance(value, (int, float)):
            symbol_limits.append((value,))
        else:
            symbol_limits.append(value)

    for symbol_values in itertools.product(*symbol_limits):
        num_new = num
        den_new = den

        # Substitute symbol values in numerator and denominator
        for i, symbol_key in enumerate(symbol_keys):
            num_new = num_new.subs(Symbol(symbol_key), symbol_values[i])
            den_new = den_new.subs(Symbol(symbol_key), symbol_values[i])

        generate_curve(num_new, den_new, s_var)

def generate_curve(num, den, s_var):
    tf = TransferFunction(num, den, s_var)     # Create the TransferFunction object
    print(f"List of Poles in this Transfer function: {tf.poles()}")
    print(f"List of Zeros in this Transfer function: {tf.zeros()}")
    bode_plot(tf, phase_unit='deg')     # Generate the bode plot
    pole_zero_plot(tf, zero_color='red', show_axes=True)     # Generate the pole-zero plot    

    # Transform to time domain
    t = Symbol('t', real=True)
    s = Symbol('s')

    # convert the transfer function to expression
    expr = tf.to_expr()

    #translate the transfer function to time domain
    time_domain_func = inverse_laplace_transform(expr, s, t)
    print(f"Time domain function: {time_domain_func}")

    # Plot the time domain function when driven by a unit step function
    step_response_plot(tf)

    # Calculate the settled response time
    settled_time = None
    cycles_to_show = 5

    if time_domain_func.poles():
        settling_time = 4 / max(time_domain_func.poles().real)
        if settling_time < float('inf'):    #checking if settling time is finite. if it does not have any poles or settling time is infinite, assign None.
            settled_time = settling_time

    if settled_time:
        print(f"Settled response time: {settled_time} seconds")
    else:
        print("Response does not settle")

        # Show 5 cycles of the lowest oscillation frequency
        if time_domain_func.zeros():
            oscillation_time = 2 * 3.14159 / min(time_domain_func.zeros().imag)
            cycles_to_show = min(cycles_to_show, int(oscillation_time))
        
        print(f"Showing {cycles_to_show} cycles")

def test_func():
    s = Symbol("s")

    #TEST: 1 POLE, 1 ZERO
    p1 = Symbol("p1")
    z1 = Symbol("z1")
    sp = z1 / (s * p1)
    limits = {"p1": (1e3, 1.4e3, 2e3), "z1":(40e3, 50e3, 60e3)}

    # TEST: LIMITS DICTIONARY HAS KEYS IN DIFFERENT ORDER
    # p1 = Symbol("p1")
    # z1 = Symbol("z1")
    # sp = z1 / (s * p1)
    # limits = {"z1":(40e3, 50e3, 60e3), "p1": (1e3, 1.4e3, 2e3)}
    
    # TEST: 2 POLES, 1 ZERO
    # p1 = Symbol("p1")
    # p2 = Symbol("p2")
    # z1 = Symbol("z1")
    # sp = z1 / (s * p1 + p2)
    # limits = {"p1": (1e3, 1.4e3, 2e3), "p2":(5e6, 7e6, 10e6), "z1":(40e3, 50e3, 60e3)}

    # TEST: USE DIFFERENT SYMBOL NAMES, NOT JUST P1, P2, P3, Z1, Z2, Z3
    # mypole1 = Symbol("mypole1")
    # myzero1 = Symbol("myzero1")
    # sp = myzero1 / (s * mypole1)
    # limits = {"mypole1": (1e3, 1.4e3, 2e3), "myzero1":(40e3, 50e3, 60e3)}

    # TEST: DIFFERNET LIMITS IN EACH SYMBOL
    # p1 = Symbol("p1")
    # p2 = Symbol("p2")
    # z1 = Symbol("z1")
    # sp = z1 / (s * p1 + p2)
    # limits = {"p1": (1e3, 1.4e3, 2e3), "p2":(5e6,), "z1":(40e3, 50e3)}

    # TEST: DIFFERNET LIMITS IN EACH SYMBOL, NUMERIC VALUE, SINGLE VALUE TUPLE, AND 2-VALUE TUPLE
    # p1 = Symbol("p1")
    # p2 = Symbol("p2")
    # z1 = Symbol("z1")
    # sp = z1 / (s * p1 + p2)
    # limits = {"p1": 1e3, "p2": (10e3,), "z1":(40e3, 50e3)}

    # TEST: '{symbol}' IN THE TRANSFER FUNCTION IS NOT FOUND IN THE LIMITS DICTIONARY (should raise VALUE error as defined)
    # p1 = Symbol("p1")
    # p2 = Symbol("p2")
    # z1 = Symbol("z1")
    # sp = z1 / (s * p1 + p2)
    # limits = {"p1": (1e3, 1.4e3, 2e3), "p2":(5e6, 7e6, 10e6), "z2":(40e3, 50e3, 60e3)} # "z1" is not defined in transfer function

    # TEST: single numeric value in limits dictionary
    # p1 = Symbol("p1")
    # sp = 1 / (s * p1)
    # limits = {"p1": 1e3}

    # TEST: 3 POLES, 3 ZEROS
    # p1 = Symbol("p1")
    # p2 = Symbol("p2")
    # p3 = Symbol("p3")
    # z1 = Symbol("z1")
    # z2 = Symbol("z2")
    # z3 = Symbol("z3")
    # sp = ((s + z1)*(s + z2)*(s + z3)) / ((s + p1)*(s + p2)*(s + p3))
    # limits = {"p1": (1e3,), "p2": (10e3,), "p3": (100e3,), "z1": (1e2, 1e4), "z2": (1e3, 1e5), "z3": (1e4, 1e6)}

    # TEST: UNIT STEP RESPONSE
    # sp = ((8*s**2 + 18*s + 32) / (s**3 + 6*s**2 + 14*s + 24))
    # limits = {}

    process_fs(sp, s, limits)

if __name__ == "__main__":
    test_func()