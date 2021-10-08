"""


"""

__author__ = "Bilal Hayat Butt, Aashir Iftikhar, Maaz Ahmed and Syed Faran Mustafa"

__license__ = """The MIT License (MIT)

Copyright (c) [2021] [Bilal Hayat Butt]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""


__version__ = "1.0.1"

def generateJournanalCitationNetworkText(fileName, outputFileName):
    pd.set_option("display.max_colwidth", 10000)
    df = pd.read_csv(fileName)
    journalCitationText = open(outputFileName,"a", encoding="utf-8")
    Graphpath = os.path.join("Article.graph")
    hashes = os.path.join("Article.hash")
    hashes = snap.TFIn(hashes)
    mapping = snap.TStrIntSH (hashes)
    FIn = snap.TFIn(Graphpath)
    G = snap.TNGraph.Load(FIn)
    
    for EI in G.Edges():
        s = df.loc[df["DOI"]==mapping.GetKey(EI.GetSrcNId())]
        d = df.loc[df["DOI"]==mapping.GetKey(EI.GetDstNId())]
        if not s.empty and not d.empty:
            source = s["Journal Name"].to_string(index=False)[1:].replace(" ","_")
            dest = d["Journal Name"].to_string(index=False)[1:].replace(" ","_")
            doiD = d["DOI"].to_string(index=False)[1:].replace(" ","_")
            doiS = s["DOI"].to_string(index=False)[1:].replace(" ","_")
            journalCitationText.write(source + "\t" + dest + "\n")
#     print("edge (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId()))
    
    print("%s is generated" % outputFileName)


def generateJournalCitationGraph(fileName, outputGraph, outputHash):
    (graph,hashes) = snap.LoadEdgeListStr(snap.TNEANet, fileName,0, 1,True) #Loading text file as EdgeList and creating hash for retrieving
    print("Number of Nodes: %d, Number of Edges: %d" % (graph.GetNodes(), graph.GetEdges())) #Checking the node count if graph is generated successfully or not.

    filename = outputGraph #Creating graph file
    FOut = snap.TFOut(filename) #Using snap's built in function to save
    graph.Save(FOut) #Saving file
    FOut.Flush() #Flushing the file value

    name = outputHash #Creating Hash file
    FOut = snap.TFOut(name) #Using snap's built in function to save
    hashes.Save(FOut) #Saving file
    FOut.Flush() #Flushing the file value
    print("Graph created %s" % outputGraph) #To make sure graph is created


def generateSubGraph(hashF, graphF, outputSubGraph, metaDataFile, newMetaDataSubFile):
    hashes = snap.TFIn(hashF)
    mapping = snap.TStrIntSH (hashes)

    graphFile = snap.TFIn(graphF)
    graph = snap.TNEANet.Load(graphFile)

    OutDegV = graph.GetNodeOutDegV() #Using Snap's OutDegree function to get OutDegrees
    InDegV = graph.GetNodeInDegV() #Using Snap's OutDegree function to get OutDegrees
    outCount = 0 #Checking if all nodes are traversed
    totalCount = 0
    outCount1 = 0
    in1 = 0
    NIdV = []
    for (item1,item2) in zip(OutDegV,InDegV): #Traversing all the Nodes
        if(item1.GetVal2()>0):
            outCount = outCount+1
            name = mapping.GetKey(item1.GetVal1()).replace("_"," ") 
            ids = item1.GetVal1() #Getting ID 
            val = item1.GetVal2() #Getting OutDegree value
            NIdV.append(ids)
            totalCount = item2.GetVal2() + totalCount
        else:
            outCount1 = outCount1+1
            in1 = in1+item2.GetVal2()
    
    print(totalCount,outCount,outCount1,in1) #Checking the count
    
    SubGraph = graph.GetSubGraph(NIdV)
    filename = outputSubGraph #Creating graph file
    FOut = snap.TFOut(filename) #Using snap's built in function to save
    SubGraph.Save(FOut) #Saving file
    FOut.Flush() #Flushing the file value
    
    df = pd.read_csv(metaDataFile)
    pd.set_option("display.max_colwidth", 10000)
    graphFile = snap.TFIn(outputSubGraph)
    graph = snap.TNEANet.Load(graphFile)
    hashes = snap.TFIn(hashF)
    mapping = snap.TStrIntSH (hashes)
    count = 0

    #df['Journal Name'] = df['Journal Name'].str.upper()
    with open(newMetaDataSubFile, 'w', newline='', encoding="utf-8") as file:
        subMeta = csv.writer(file) #Using CSV writer
        subMeta.writerow(['Article Name','Author Name', 'DOI', 'ISSN', 'ISBN', 'Journal Name', 'Date']) 

    for N in graph.Nodes():
        count = count+1
        name = mapping.GetKey(N.GetId()).replace("_"," ")
        data = df.loc[(df["Journal Name"]==name)]
        data.to_csv(newMetaDataSubFile, mode='a', header=False)
    print(count)


def generateAuthorArticleCitationNetworkText(metaDataFile, outputAuthorFile, outputArticleFile):
    pd.set_option("display.max_colwidth", 10000)
    df = pd.read_csv(metaDataFile)
    articleCitationText = open(outputArticleFile,"w", encoding="utf-8")
    authorCitationText = open(outputAuthorFile,"w", encoding="utf-8")
    Graphpath = os.path.join("Article.graph")
    hashes1 = os.path.join("Article.hash")
    hashes = snap.TFIn(hashes1)
    mapping = snap.TStrIntSH (hashes)
    FIn = snap.TFIn(Graphpath)
    G = snap.TNGraph.Load(FIn)
    for EI in G.Edges():
        s = df.loc[df["DOI"]==mapping.GetKey(EI.GetSrcNId())]
        d = df.loc[df["DOI"]==mapping.GetKey(EI.GetDstNId())]
        if not s.empty and not d.empty:
            source = s["Article Name"].to_string(index=False)[1:].replace(" ","_")
            dest = d["Article Name"].to_string(index=False)[1:].replace(" ","_")
            articleCitationText.write(source + " " + dest + "\n")
            source = s["Author Name"].to_string(index=False)[1:].replace(" ","_")
            dest = d["Author Name"].to_string(index=False)[1:].replace(" ","_")
            author1  = source.split(",")
            author2  = dest.split(",")
            del author1[0]
            del author2[0]    
            if author2:
                if((type(author1) is str) and (type(author2) is str)): #IF there are only single authors
                        auth1 = author1.replace (" ", "_") #Replacing spaces with underscores.
                        auth2 = author2.replace (" ", "_") #Replacing spaces with underscores.
                        authorCitationText.write(auth1.upper() + " " + auth2.upper()) #Writing it to a file
                        authorCitationText.write("\n") #Writing next line
                elif((type(author1) is str) and (type(author2) is list)): #If one author is single and 2nd is list
                        for x in author2: #Traversing each author
                            auth1 = author1.replace (" ", "_") #Replacing spaces with underscores.
                            auth2 = x.replace (" ", "_") #Replacing spaces with underscores.
                            authorCitationText.write(auth1.upper() + " " + auth2.upper()) #Writing it to a file
                            authorCitationText.write("\n") #Writing next line
                elif((type(author1) is list) and (type(author2) is str)): #If 1st author is list and second is single
                        for x in author1: #Traversing each author
                            auth1 = x.replace (" ", "_") #Replacing spaces with underscores.
                            auth2 = author2.replace (" ", "_") #Replacing spaces with underscores.
                            authorCitationText.write(auth1.upper() + " " + auth2.upper()) #Writing it to a file
                            authorCitationText.write("\n") #Writing next line
                elif((type(author1) is list) and (type(author2) is list)): #If both authors are list
                        for x in author1: #Checking for each value in first author
                            for y in author2: #Then for each value in second author
                                auth1 = x.replace (" ", "_") #Replacing spaces with underscores.
                                auth2 = y.replace (" ", "_") #Replacing spaces with underscores.
                                if auth2:
                                    authorCitationText.write(auth1.upper() + " " + auth2.upper()) #Writing it to a file.
                                    authorCitationText.write("\n") #Writing next line.
    
    print("%s & %s is Generated" % (outputAuthorFile, outputArticleFile))


def generateAuthorArticleGraph(authorFile, outputAuthorGraphFile, outputAuthorHashFile, articleFile, 
                               outputArticleGraphFile, outputArticleHashFile):
    (graph,hashes) = snap.LoadEdgeListStr(snap.TNEANet, authorFile,0, 1,True) #Loading text file as EdgeList and creating hash for retrieving
    print("Number of Nodes: %d, Number of Edges: %d" % (graph.GetNodes(), graph.GetEdges())) #Checking the node count if graph is generated successfully or not.

    filename = outputAuthorGraphFile#Creating graph file
    FOut = snap.TFOut(filename) #Using snap's built in function to save
    graph.Save(FOut) #Saving file
    FOut.Flush() #Flushing the file value

    name = outputAuthorHashFile #Creating Hash file
    FOut = snap.TFOut(name) #Using snap's built in function to save
    hashes.Save(FOut) #Saving file
    FOut.Flush() #Flushing the file value

    print("Graph created") #To make sure graph is created   
    
    (graph,hashes) = snap.LoadEdgeListStr(snap.TNEANet, articleFile,0, 1,True) #Loading text file as EdgeList and creating hash for retrieving
    print("Number of Nodes: %d, Number of Edges: %d" % (graph.GetNodes(), graph.GetEdges())) #Checking the node count if graph is generated successfully or not.

    filename = outputArticleGraphFile #Creating graph file
    FOut = snap.TFOut(filename) #Using snap's built in function to save
    graph.Save(FOut) #Saving file
    FOut.Flush() #Flushing the file value

    name = outputArticleHashFile #Creating Hash file
    FOut = snap.TFOut(name) #Using snap's built in function to save
    hashes.Save(FOut) #Saving file
    FOut.Flush() #Flushing the file value


    print("Graph created %s & %s"% (outputAuthorGraphFile, outputArticleGraphFile)) #To make sure graph is created


def generateAuthorJournalRank(authorHash, authorGraph, outputAuthorFile, journalHash, journalGraph, outputJournalFile, JournalGraphStatsF, AuthorGraphStatsF):
    authorHashes = snap.TFIn(authorHash) #Loading hash file
    authorMapping = snap.TStrIntSH (authorHashes) #Creating mapping list containing NodeIDs and Names
    graphFile = snap.TFIn(authorGraph) #Loading graph file.
    authorGraph = snap.TNEANet.Load(graphFile) #Loading graph file into variable
    snap.PrintInfo(authorGraph, "Python type PUNGraph", AuthorGraphStatsF, False)
    
    PageRankH = snap.TIntFltH() #Creating Integer float hash for PR
    snap.GetPageRank(authorGraph, PageRankH, 0.85, 1e-8, authorGraph.GetNodes()) #Saving PageRank of the graph in var created above.
    
    InDegV = authorGraph.GetNodeInDegV() #Using Snap's InDegree function to get InDegrees
    OutDegV = authorGraph.GetNodeOutDegV() #Using Snap's OutDegree function to get OutDegrees
    with open(outputAuthorFile, 'w', newline='', encoding="utf-8") as file: #Creating file AuthorCitationInfo.csv
        authorcsv = csv.writer(file) #Using CSV writer
        authorcsv.writerow(['Author Name', 'Rank', 'Citation']) #Writing the column names
        for (item1,item2,item3) in zip(PageRankH,InDegV,OutDegV): #Traversing all the items in PageRank Hash
            pr = PageRankH[item1] #Separating PageRank using subscript. here item is NodeID
            name = authorMapping.GetKey(item1).replace("_"," ") #Using mapping hash separating the Name of author
            authorcsv.writerow([name,pr,item2.GetVal2()]) #Writing NodeID, Author Name, PR Score
    
    print("Author Ranking Completed") #Checking when PR is done
    
    
    hashes = snap.TFIn(journalHash) #Loading hash file
    mapping = snap.TStrIntSH (hashes) #Creating mapping list containing NodeIDs and Names
    
    graphFile = snap.TFIn(journalGraph) #Loading graph file.
    graph = snap.TNEANet.Load(graphFile) #Loading graph file into variable
    
    snap.PrintInfo(graph, "Python type PUNGraph", JournalGraphStatsF, False)
    
    PageRankH = snap.TIntFltH() #Creating Integer float hash for PR
    snap.GetPageRank(graph, PageRankH, 0.85, 1e-8, graph.GetNodes()) #Saving PageRank of the graph in var created above.
    

    InDegV = graph.GetNodeInDegV() #Using Snap's InDegree function to get InDegrees
    OutDegV = graph.GetNodeOutDegV() #Using Snap's OutDegree function to get OutDegrees
    with open(outputJournalFile, 'w', newline='', encoding="utf-8") as file: #Creating file AuthorCitationInfo.csv
        journalcsv = csv.writer(file) #Using CSV writer
        journalcsv.writerow(['Journal Name', 'Rank', 'Citation']) #Writing the column names
        for (item1,item2,item3) in zip(PageRankH,InDegV,OutDegV): #Traversing all the items in PageRank Hash
            pr = PageRankH[item1] #Separating PageRank using subscript. here item is NodeID
            name = mapping.GetKey(item1).replace("_"," ") #Using mapping hash separating the Name of author
            journalcsv.writerow([name,pr,item2.GetVal2()]) #Writing NodeID, Author Name, PR Score
    
    print("Journal Ranking Completed") #Checking when PR is done


def generateArticleRank(journalFile, metaDataFile, articlegraph, articleHash, authorFile, outputFile, ArticleGraphStatsF):
    pd.set_option("display.max_colwidth", 10000)
    journal = pd.read_csv(journalFile)
    author = pd.read_csv(authorFile)
    df = pd.read_csv(metaDataFile)

    #df['Article Name'] = df['Article Name'].str.upper()

    graphFile = snap.TFIn(articlegraph)
    graph = snap.TNEANet.Load(graphFile)
    hashes = snap.TFIn(articleHash)
    mapping = snap.TStrIntSH (hashes)

    snap.PrintInfo(graph, "Python type PUNGraph", ArticleGraphStatsF, False)
    
    InDegV = graph.GetNodeInDegV() #Using Snap's InDegree function to get InDegrees
    OutDegV = graph.GetNodeOutDegV() #Using Snap's OutDegree function to get OutDegrees
    with open(outputFile, 'w', newline='', encoding="utf-8") as file:
        multi = csv.writer(file) #Using CSV writer
        multi.writerow(['Article Name', 'Rank', 'Citation']) #Writing the column names
        for (item1,item2) in zip(InDegV,OutDegV):
            s = df.loc[df["Article Name"]==mapping.GetKey(item1.GetVal1()).replace("_"," ")]
            journalName = s["Journal Name"].to_string(index=False)[1:]
            authors = s["Author Name"].to_string(index=False)[1:].split(",")
            journalScore = journal.loc[journal["Journal Name"]==journalName]
            articleName = s["Article Name"].to_string(index=False)[1:]
            del(authors[0])
            if not journalScore.empty:
                jPr = float(journalScore["Rank"].to_string(index=False)[1:])
                aPr = 0
                totalScore = 0
                for i in (authors):
                    authorScore = author.loc[author["Author Name"]==i.upper()]
                    if not authorScore.empty:
                        aPr = aPr + float(authorScore["Rank"].to_string(index=False)[1:])
                totalScore = aPr*0.5 + jPr*0.5
                multi.writerow([articleName,totalScore,item1.GetVal2()])
                
    print("Article Ranking Completed")


def generateTemporalNetwork(metaData,RankYearStart,RankYearEnd, CutOffStart, CutOffEnd, metaDataRankYearCSV, 
                            metaDataCutOffYearCSV, ArticleHash, ArticleGraph):
    graphFile = snap.TFIn(ArticleGraph)
    graph = snap.TNEANet.Load(graphFile)
    hashes = snap.TFIn(ArticleHash)
    mapping = snap.TStrIntSH (hashes)

    lst = []
    for N in graph.Nodes():
        name = mapping.GetKey(N.GetId()).replace("_"," ")
        lst.append(name)
    df = pd.read_csv(metaData)
    df = df[df["Article Name"].isin(lst)]

   
    dfRank = df[(df.Date >= RankYearStart) & (df.Date <= RankYearEnd)]
    
    with open(metaDataRankYearCSV, 'w', newline='', encoding="utf-8") as file:
        subMeta = csv.writer(file) #Using CSV writer
        subMeta.writerow(['Article Name','Author Name', 'DOI', 'ISSN', 'ISBN', 'Journal Name', 'Date'])
           
    dfRank.to_csv(metaDataRankYearCSV, mode='a', header=False)
        
    
    dfCutOff = df[(df.Date >= CutOffStart) & (df.Date <= CutOffEnd)]
    
    with open(metaDataCutOffYearCSV, 'w', newline='', encoding="utf-8") as file:
        subMeta = csv.writer(file) #Using CSV writer
        subMeta.writerow(['Article Name','Author Name', 'DOI', 'ISSN', 'ISBN', 'Journal Name', 'Date'])
        
    dfCutOff.to_csv(metaDataCutOffYearCSV, mode='a', header=False)
    print("Metadata created %s & %s"% (metaDataRankYearCSV, metaDataCutOffYearCSV)) #To make sure graph is created


def generateGraphStats(journalGraph, articleGraph, authorGraph, outputF):    
    
    i = 0
    with open(outputF, 'w', newline='', encoding="utf-8") as file: #Creating file ArtcileOutDegreeInfo.csv
        out = csv.writer(file) #Using CSV writer
        out.writerow(['Attributes',authorGraph, articleGraph, journalGraph]) #Writing the column names

        with open(authorGraph,'r', encoding="utf-8") as myfile,         open(articleGraph,'r', encoding="utf-8") as myfile2,         open(journalGraph, 'r', encoding="utf-8") as myfile3:

                 for myline, myline2, myline3 in zip(myfile, myfile2, myfile3):#Reading it line by line
                        if i == 0:
                            i += 1
                            continue
                        myline = myline.strip() #Stripping the line
                        myline = re.split(':',myline) #Converting it into array by splitting with "Tabs"
                        paper1 = myline[1] #Since it has 2 columns citing and cited paper. Taking first column as Paper1
                    
                        myline2 = myline2.strip() #Stripping the line
                        myline2 = re.split(':',myline2) #Converting it into array by splitting with "Tabs"
                        paper2 = myline2[1] #Since it has 2 columns citing and cited paper. Taking first column as Paper1
                    
                        myline3 = myline3.strip()
                        myline3 = re.split(':',myline3)
                        paper3 = myline3[1]
                        #print(paper1.strip()," - ",paper2.strip())
                        out.writerow([myline[0],paper1.strip(),paper2.strip(), paper3.strip()]) #Writing NodeID, Artcile Name, OutDegree Value


def correlationAnalysis(AuthorInfoCSV, AuthorCutOffYearInfoCSV, JournalInfoCSV, 
            JournalCutOffYearInfoCSV, ArticleInfoCSV, ArticleCutOffYearInfoCSV, metaDataRankYearCSV):
    df = pd.read_csv(metaDataRankYearCSV, usecols=["Article Name","Journal Name","Author Name"], dtype={"Article Name": str,"Journal Name":str,"Author Name":str})    
    df=df.dropna()

                                        ###Author Correlation###
       
    a = list(set([i.strip() for i in ','.join(df["Author Name"]).upper().split(',')]))
    del a[0]
    #print (a)
    df1 = pd.read_csv(AuthorInfoCSV)
    #print (df1.count(),df1)
    df1 = df1[df1["Author Name"].isin(a)]
    #print (df1.count(),df1)
           
    df2 = pd.read_csv(AuthorCutOffYearInfoCSV)
    #print (df2.count(),df2)
    df2 = df2[df2["Author Name"].isin(a)]
    #print (df2.count(),df2)
    
    df_suffix = pd.merge(df1, df2, left_on="Author Name",right_on="Author Name",how='inner',suffixes=('_Total','_Early'))
    df_suffix.drop("Author Name", axis='columns', inplace=True) 
    print ("Correlation analysis for total %d Authors" % len(df_suffix.index))
    
    correlation_mat = df_suffix.rank().corr()
    sns.heatmap(correlation_mat, annot = True)
    plt.title("Author Correlation matrix", y=-0.75)
    #plt.xlabel("cell nucleus features")
    #plt.ylabel("cell nucleus features")
    plt.show()
      
    corr, _ = spearmanr(df_suffix['Rank_Total'].rank(), df_suffix['Rank_Early'].rank())
    print('Author Correlation between Total Rank and Early Rank = %.3f' % corr)
    
    corr, _ = spearmanr(df_suffix['Citation_Total'].rank(), df_suffix['Citation_Early'].rank())
    print('Author Correlation between Total Citation and Early Citation = %.3f' % corr)
    
    corr, _ = spearmanr(df_suffix['Citation_Early'].rank(), df_suffix['Rank_Total'].rank())
    print('Author Correlation between Early Citation and Total Rank = %.3f' % corr)
    
    corr, _ = spearmanr(df_suffix['Citation_Total'].rank(), df_suffix['Rank_Total'].rank())
    print('Author Correlation between Total Citation and Total Rank = %.3f' % corr)
    
    corr, _ = spearmanr(df_suffix['Citation_Early'].rank(), df_suffix['Rank_Early'].rank())
    print('Author Correlation between Early Rank and Early Citation = %.3f' % corr)
    
    corr, _ = spearmanr(df_suffix['Rank_Early'].rank(), df_suffix['Citation_Total'].rank())
    print('Author Correlation between Early Rank and Total Citation = %.3f' % corr)
    
    g = sns.PairGrid(df_suffix.rank())
    g.map_upper(plt.scatter)
    g.map_lower(sns.kdeplot, cmap = "Blues_d")
    g.map_diag(sns.kdeplot, lw = 3, legend = False);
    plt.show()
    
    print(" ")
    print(" ")
    
    
                                        ###Journal Correlation###
    j = df["Journal Name"].dropna().unique()
        
    df1 = pd.read_csv(JournalInfoCSV)
    #print (df1.count())
    df1 = df1[df1["Journal Name"].isin(j)]
    #print (df1.count())
    
    df2 = pd.read_csv(JournalCutOffYearInfoCSV)
    #print (df2.count())
    df2 = df2[df2["Journal Name"].isin(j)]
    #print (df2.count())
    
    df_suffix = pd.merge(df1, df2, left_on="Journal Name",right_on="Journal Name",how='inner',suffixes=('_Total','_Early'))
    #print (df_suffix.count())
    # calculate Pearson's correlation
    df_suffix.drop("Journal Name", axis='columns', inplace=True) 
    print ("Correlation analysis for total %d Journals" % len(df_suffix.index))
    
    correlation_mat = df_suffix.rank().corr()
    sns.heatmap(correlation_mat, annot = True)
    plt.title("Journal Correlation matrix", y=-0.75)
    #plt.xlabel("cell nucleus features")
    #plt.ylabel("cell nucleus features")
    plt.show()
    
     
    corr, _ = spearmanr(df_suffix['Rank_Total'].rank(), df_suffix['Rank_Early'].rank())
    print('Journal Correlation between Total Rank and Early Rank = %.3f' % corr)
    #pyplot.scatter(df_suffix['Rank_Total'].rank(), df_suffix['Rank_Early'].rank())
    #pyplot.show()
    
    corr, _ = spearmanr(df_suffix['Citation_Total'].rank(), df_suffix['Citation_Early'].rank())
    print('Journal Correlation between Total Citation and Early Citation = %.3f' % corr)
    
    corr, _ = spearmanr(df_suffix['Citation_Early'].rank(), df_suffix['Rank_Total'].rank())
    print('Journal Correlation between Early Citation and Total Rank = %.3f' % corr)
    
    corr, _ = spearmanr(df_suffix['Citation_Total'].rank(), df_suffix['Rank_Total'].rank())
    print('Journal Correlation between Total Citation and Total Rank = %.3f' % corr)
    
    corr, _ = spearmanr(df_suffix['Citation_Early'].rank(), df_suffix['Rank_Early'].rank())
    print('Journal Correlation between Early Rank and Early Citation = %.3f' % corr)
    
    corr, _ = spearmanr(df_suffix['Rank_Early'].rank(), df_suffix['Citation_Total'].rank())
    print('Journal Correlation between Early Rank and Total Citation = %.3f' % corr)
    g = sns.PairGrid(df_suffix.rank())
    g.map_upper(plt.scatter)
    g.map_lower(sns.kdeplot, cmap = "Blues_d")
    g.map_diag(sns.kdeplot, lw = 3, legend = False);
    plt.show()
       
    print(" ")
    print(" ")
                                        ###Article Correlation###
    ar = (df["Article Name"]).dropna().unique()
    
    df1 = pd.read_csv(ArticleInfoCSV)
    #print (df1.count())
    df1 = df1[df1["Article Name"].isin(ar)]
    #print (df1.count())
    
    df2 = pd.read_csv(ArticleCutOffYearInfoCSV)
    #print (df2.count())
    df2 = df2[df2["Article Name"].isin(ar)]
    #print (df2.count())
    
    df_suffix = pd.merge(df1, df2, left_on="Article Name",right_on="Article Name",how='inner',suffixes=('_Total','_Early'))
    df_suffix.drop("Article Name", axis='columns', inplace=True) 
    print ("Correlation analysis for total %d Articles" % len(df_suffix.index))
    
    correlation_mat = df_suffix.rank().corr()
    sns.heatmap(correlation_mat, annot = True)
    plt.title("Article Correlation matrix", y=-0.75)
    #plt.xlabel("cell nucleus features")
    #plt.ylabel("cell nucleus features")
    plt.show()
        
      
    # calculate Pearson's correlation
    corr, _ = spearmanr(df_suffix['Rank_Total'].rank(), df_suffix['Rank_Early'].rank())
    print('Article Correlation between Total Rank and Early Rank = %.3f' % corr)
    #pyplot.scatter(df_suffix['Rank_Total'].rank(), df_suffix['Rank_Early'].rank())
    #pyplot.show()
    
    corr, _ = spearmanr(df_suffix['Citation_Total'].rank(), df_suffix['Citation_Early'].rank())
    print('Article Correlation between Total Citation and Early Citation = %.3f' % corr)
    #pyplot.scatter(df_suffix['Citation_Total'].rank(), df_suffix['Citation_Early'].rank())
    #pyplot.show()
    
    corr, _ = spearmanr(df_suffix['Citation_Early'].rank(), df_suffix['Rank_Total'].rank())
    print('Article Correlation between Early Citation and Total Rank = %.3f' % corr)
    
    corr, _ = spearmanr(df_suffix['Citation_Total'].rank(), df_suffix['Rank_Total'].rank())
    print('Article Correlation between Total Citation and Total Rank = %.3f' % corr)
    
    corr, _ = spearmanr(df_suffix['Citation_Early'].rank(), df_suffix['Rank_Early'].rank())
    print('Article Correlation between Early Rank and Early Citation = %.3f' % corr)
    
    corr, _ = spearmanr(df_suffix['Rank_Early'].rank(), df_suffix['Citation_Total'].rank())
    print('Article Correlation between Early Rank and Total Citation = %.3f' % corr)

    g = sns.PairGrid(df_suffix.rank())
    g.map_upper(plt.scatter)
    g.map_lower(sns.kdeplot, cmap = "Blues_d")
    g.map_diag(sns.kdeplot, lw = 3, legend = False);
    plt.show()
    
    
    reference = df_suffix['Rank_Total'].rank()
    hypothesis = df_suffix['Rank_Early'].rank()
    
    print("\t TRDCG:\t\t\t{0}".format(measures.find_dcg(reference)))
    print("\t ERDCG:\t\t\t{0}".format(measures.find_dcg(hypothesis)))
    print("\t nDCG:\t\t\t{0}".format(measures.find_ndcg(reference, hypothesis)))
    print("\t Precision:\t\t{0}".format(measures.find_precision(reference, hypothesis)))
    print("\t Precision at k:\t{0}".format(measures.find_precision_k(reference, hypothesis, len(reference))))
    print("\t Average precision:\t{0}".format(measures.find_average_precision(reference, hypothesis)))
    print("\t RankDCG:\t\t{0}".format(measures.find_rankdcg(reference, hypothesis), "\n"))