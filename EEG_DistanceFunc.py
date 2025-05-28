def DistanceFunc(selectedPoint, pointArray, responseArray, nNearest):
    import numpy as np
    import statistics
    
    """
    

    Parameters
    ----------
    selectedPoint : List of Int
        The coordinates of the point to create a definition (unit amount) for
    pointArray : List of List of Int
        List of Coordinates of all points currently described in the system
    responseArray : List of Int
        Unit values, in order, for all points within the point array 
    nNearest : Int
        Number of nearest points to select as influential for the distance model,
        larger int values drastically slow down the speed for >1000 nodal points.
        Suggestion 5-10 nearest for best results
        

    Returns
    -------
    np.random.normal(loc=weightedAverage, scale = statistics.stdev(responseArray)) :
        A value determined based on the mean and standard deviation of the weighted averages
        found via the distance function. This output is used in the EEG_Plotting Function

    """
    
    #Creates list objects to store all nearest values and coordinates
    nNearestNet = [10] * nNearest 
    nNearestSupply = [[0,0,0]]*nNearest

    
    #For loop checks distances of all points in pointArray to determine n closest "neighbor" points
    #It then assigns their values and coordinates to two list objects
    for walk in range(len(pointArray)):
        for fill in range(nNearest):
            if abs(selectedPoint[0]-pointArray[walk][0]) + abs(selectedPoint[1]-pointArray[walk][1])+ + abs(selectedPoint[2]-pointArray[walk][2])<nNearestNet[fill]:
                nNearestNet[fill] = abs(selectedPoint[0]-pointArray[walk][0]) + abs(selectedPoint[1]-pointArray[walk][1])+ abs(selectedPoint[2]-pointArray[walk][2])
                nNearestSupply[fill] = [pointArray[walk][0],pointArray[walk][1]]
                break
    
    #Correction for the in use datapoints to select only nearest neighbors for use
    DelBoolean = np.isin(pointArray, nNearestSupply)
    
    for responseCategory in range(len(DelBoolean)):
        if not DelBoolean[responseCategory].all:
            responseArray[responseCategory] = []
        
    #Finalizes a "weighted average" based on net coordinate distance from the point
    weightedAverage = 0
    for elementA in range(len(nNearestSupply)):
        intAvg = nNearestNet[elementA]/sum(nNearestNet)
        weightedAverage+= intAvg * responseArray[elementA]

    #The value returned uses weighted average as the mean, and the whole of the Corrected Response array to find a standard deviation from
    return np.random.normal(loc=weightedAverage, scale = statistics.stdev(responseArray))
