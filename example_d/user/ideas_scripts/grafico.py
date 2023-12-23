import matplotlib.pyplot as plt
# https://www.includehelp.com/python/dot-plot.aspx#:~:text=The%20dot%20plot%20is%20a%20type%20of%20data,plots%20are%20majorly%20used%20in%20clustering%20data%20analysis.
'''
X = [1, 2, 3, 4, 5]
#Y = [5, 6.4, 6.5, 7.6, 2]
X = [1, 1, 2]
Y = [1, 1, 1]

plt.figure()
plt.plot(X, Y)

for i in range(len(X)):
    #plt.annotate(str(Y[i]), xy=(X[i], Y[i]))
    plt.annotate(str(X[i]), xy=(X[i], Y[i]))

plt.savefig("migrafico.png")
#plt.show()
'''
# plotting using plt.pyplot()
plt.plot([4,7,3,6,1,8,9,2,3], 'ro')
#plt.plot([13], 'yo')
plt.plot([1,7,3,6,8,42,34,62],[1,8,9,3,10,11,12,13], 'yo')

# axis labeling
plt.xlabel('numbers')
plt.ylabel('values')

# figure name
plt.title('Dot Plot : Red Dots')
plt.savefig("migrafico.png")

##########################################
##########################################
