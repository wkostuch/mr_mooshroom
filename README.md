# Mr. Mooshroom: 2021 MCM Problem A

The COMAP **Mathematical Contest in Modeling**, or MCM, is a yearly competition run by the *Consortium for Mathematics and Its Applications*.  The contest takes place over four days and tasks the participating teams (each comprised of three students) to answer one of six problems.  The "answer" to a problem is a ~20 page research paper based on the results of the model built by the team to describe the phenonmenon in question.  The research, construction, testing, and validation of the model as well as the writing and submission of the research paper must be completed by the end of the 4th day.

Questions in the past have been quite varied, including: "What's the best shape for a sandcastle?", "How much do the leaves on a tree weigh?", "What's the best approach to eradicating ebola?", and "What's the best way to manage Kariba Dam on the Zambezi River?", among others throughout the years.  

The question this team chose to answer for the 2021 competition was **Problem A: Fungi**.  The question's requirements are listed below:
 
> - Build a mathematical model that describes the breakdown of ground litter and woody fibers through fungal activity in the presence of multiple species of fungi.
> - In your model, incorporate the interactions between different species of fungi, which have different growth rates and different moisture tolerances as shown in Figures 1 and 2.
> - Provide an analysis of the model and describe the interactions between the different types of fungi. The dynamics of the interactions should be characterized and described including both short- and long-term trends. Your analysis should examine the sensitivity to rapid fluctuations in the environment, and you should determine the overall impact of changing atmospheric trends to assess the impact of variation of local weather patterns.
> - Include predictions about the relative advantages and disadvantages for each species and combinations of species likely to persist, and do so for different environments including arid, semi-arid, temperate, arboreal, and tropical rain forests.
> - Describe how the diversity of fungal communities of a system impacts the overall efficiency of a system with respect to the breakdown of ground litter. Predict the importance and role of biodiversity in the presence of different degrees of variability in the local environment.

To answer this question, we built a model in Python that implements a model for different species of fungi and different environments.  The following flowchart depicts how the model works in broad strokes:

![Model flowchart](https://user-images.githubusercontent.com/37635286/110566974-67764580-8116-11eb-876d-a35b3c2bfb11.png)

The results of the model are striking and, more importantly, agree with published literature on the topic of organic decompsition and fungi growth.  We built a tool that turns the model's results into a heatmap, where different colors correspond to different fungi and the opacity of a given cell corresponds to how much organic mass the fungi has decomposed in that cell.  Here is a figuring showing the results after one year:
![Model results after one year.](https://user-images.githubusercontent.com/37635286/110567536-51b55000-8117-11eb-94ae-dcf8e21fac9e.png)
Here a figure showing the change after another year (two years of total fungal growth):
![Model results after two years.](https://user-images.githubusercontent.com/37635286/110567652-79a4b380-8117-11eb-99b4-c275c2b41995.png)

As the two figures show, our model realistically models and depicts fungal growth in different climates with different species of fungus interacting.  For more details, please read the "MCM 2021.pdf" found in this repository.  
