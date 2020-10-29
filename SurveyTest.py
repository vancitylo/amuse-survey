def price_sensitivity_meter(df, interpolate=False):
    # convert data from wide to long
    # calculate frequency of each price for each group
    df1 = (df[['Too Cheap', 'Cheap', 'Expensive', 'Too Expensive']]
           .unstack()
           .reset_index()
           .rename(columns={'level_0': 'label', 0: 'prices'})[['label', 'prices']]
           .groupby(['label', 'prices'])
           .size()
           .reset_index()
           .rename(columns={0: 'frequency'})
           )
    # calculate cumsum percentages
    df1['cumsum'] = df1.groupby(['label'])['frequency'].cumsum()
    df1['sum'] = df1.groupby(['label'])['frequency'].transform('sum')
    df1['percentage'] = 100 * df1['cumsum'] / df1['sum']
    # convert data from long back to wide
    df2 = df1.pivot_table('percentage', 'prices', 'label')

    # take linear values in missing values
    if interpolate:
        df3 = df2.interpolate().fillna(0)
        df3['Too Cheap'] = 100 - df3['Too Cheap']
        df3['Cheap'] = 100 - df3['Cheap']
        plot = df3.hvplot(x='prices',
                          y=['Too Cheap', 'Cheap', 'Expensive', 'Too Expensive'],
                          ylabel='Percentage',
                          height=400,
                          color=['green', 'lightgreen', 'lightpink', 'crimson']
                          ).opts(legend_position='bottom')

    # forward fill 
    else:
        df3 = df2.ffill().fillna(0)

        df3['Too Cheap'] = 100 - df3['Too Cheap']
        df3['Cheap'] = 100 - df3['Cheap']
        plot = df3.hvplot.step(x='prices',
                               y=['Too Cheap', 'Cheap', 'Expensive', 'Too Expensive'],
                               where='post',
                               ylabel='Percentage',
                               height=400,
                               color=['green', 'lightgreen', 'lightpink', 'crimson']
                               ).opts(legend_position='bottom')
    df3['optimal_diff'] = (df3['Too Cheap'] - df3['Too Expensive'])
    df3['left_diff'] = (df3['Too Cheap'] - df3['Expensive'])
    df3['right_diff'] = (df3['Too Expensive'] - df3['Cheap'])
    optimal = df3[df3['optimal_diff'] <= 0].index[0]
    lower_bound = df3[df3['left_diff'] <= 0].index[0]
    upper_bound = df3[df3['right_diff'] >= 0].index[0]

    optimal_line = hv.VLine(optimal).opts(color='blue', line_dash='dashed', line_width=0.4)

    lower_line = hv.VLine(lower_bound).opts(color='grey', line_dash='dashed', line_width=0.4)
    upper_line = hv.VLine(upper_bound).opts(color='grey', line_dash='dashed', line_width=0.4)

    print(f'Optimal Price: ${optimal}')
    print(f'Acceptable Price Range: ${lower_bound} to ${upper_bound}')

    return plot * lower_line * optimal_line * upper_line