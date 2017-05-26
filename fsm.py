import openturns as ot
from openturns.viewer import View
import numpy as np

def functional_scatter_matrix(x, y, operator, color="blue",
                              q_levels=None, values=None, colors=None):
    def _highlight_plot(view, x_array, y_array, operator, y_values, colors):
        # Find corresponding indices
        if colors is None or len(colors) != len(y_values):
            from matplotlib.colors import cnames
            lcolors = list(cnames.keys())
            i = ot.RandomGenerator.IntegerGenerate(len(y_values), len(lcolors))
            colors = [lcolors[_] for _ in i]
        dim = len(x_array[0])
        for k, val in enumerate(y_values):
            I = np.array([operator(_[0], val) for _ in y_array])
            indices = np.where(I)[0]
            if len(indices) > 0:
                for i in range(dim):
                    x = x_array[:,i]
                    z = y_array[:,0]
                    index_i_i =  1 + i * dim + i
                    view._ax[index_i_i].plot(x[indices], z[indices], '.', color=colors[k])
                    for j in range(i + 1, dim):
                        y = x_array[:,j]
                        index_i_j =  1 + i * dim + j
                        index_j_i =  1 + j * dim + i
                        view._ax[index_i_j].plot(x[indices],y[indices], '.', color=colors[k])
                        view._ax[index_j_i].plot(y[indices],x[indices], '.', color=colors[k])
        return view

    # Functional scatter matrix
    X = ot.NumericalSample(x)
    dim = X.getDimension()
    X.setDescription([""] * dim)
    Y = ot.NumericalSample(y)
    assert(len(X) == len(Y))
    assert Y.getDimension() == 1
    if q_levels is not None and values is not None:
        raise ValueError("Expected q_Levels or values or no one")
    # Start the graphs
    p = ot.Pairs(X)
    p.setColor(color)
    g = ot.Graph()
    g.add(p)
    view = View(g)
    for i in range(dim):
        index_i_i =  1 + i * dim + i
        view._ax[index_i_i] = view._fig.add_subplot(dim, dim, index_i_i)
        view._ax[index_i_i].plot(X[:, i], Y, '.', color=color)

    # Now we get the view
    if q_levels is not None:
        # check q_level type
        if type(q_levels) is float:
            values = list(Y.computeQuantile(q_levels))
        else:
            values = [Y.computeQuantile(q)[0] for q in q_levels]
        return _highlight_plot(view, np.array(X), np.array(Y), operator, values, colors)
    elif values is not None:
        # check values
        if type(values) is float:
            values = [values]
        else:
            values = list(values)
        return _highlight_plot(view, np.array(X), np.array(Y), operator, values, colors)
    else:
        return view



if __name__ == '__main__':
    import openturns as ot
    from math import sin, pi

    dimension = 3
    a = 7.0
    b = 0.1

    # Create the Ishigami function
    input_variables = ["xi1","xi2","xi3"]
    output_variables = ["y"]
    formula = ["sin(xi1) + (" + str(a) + ") * (sin(xi2)) ^ 2 + (" + str(b) + ") * xi3^4 * sin(xi1)"]
    ishigami_model = ot.NumericalMathFunction(input_variables, output_variables, formula)
    ishigami_model.setName("Ishigami")
    # Distribution
    marginals = dimension * [ot.Uniform(-pi, pi)]
    ishigami_distribution = ot.ComposedDistribution(marginals)

    # X and Y
    X = ishigami_distribution.getSample(100000)
    Y = ishigami_model(X)
    q = Y.computeQuantile(0.95)
    view = functional_scatter_matrix(X, Y, ot.GreaterOrEqual() , color="blue",
                                     values=q, colors =["red"])