from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

model1 = "/Users/vpilone/Documents/Classes SP25/CMPSC 497/Final Project/python/trainedModel/checkpoint-3"
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B")

defaultString = "Given the research question in Question, create an Artificial Intelligence Apporach to solve it in Approach. \n\nQuestion: "
question1 = "How can we develop a self-supervised representation learning framework that learns robust and generalizable feature representations from unlabeled data, enabling effective downstream classification tasks without reliance on large labeled datasets?"
question2 = "How can a knowledge graph embedding model effectively capture semantic hierarchies in knowledge graphs to improve link prediction accuracy, particularly distinguishing between entities at different hierarchical levels and entities at the same level?"
question3 = "How can machine learning models maintain reliability and accuracy when operating in environments where the input data significantly deviates from the training data distribution, thereby mitigating catastrophic failures and ensuring robust performance?"
question4 = "For most academic conferences, authors first submit initial papers, and then get reviews from some human reviewers. If the paper is accepted, the authors are required to submit a camera-ready version after modifying based on some required damaging issues. How can AI be used to analyze how well authors followed the reviews to modify papers in camera-ready versions?"

inputs1 = defaultString + question1
inputs2 = defaultString + question2
inputs3 = defaultString + question3
inputs4 = defaultString + question4

inputs = [inputs1, inputs2, inputs3, inputs4]


pipelineGenerator = pipeline(
    "text-generation",
    model=model1,
)

for input in inputs:
    # try:
    #     response = pipelineGenerator(input)
    # except:
    response = "error"

    with open(
        "/Users/vpilone/Documents/Classes SP25/CMPSC 497/Final Project/python/modelOutputs.txt",
        "+a",
    ) as outputFiles:
        outputFiles.write("Input " + str(inputs.index(input)) + ":\n")
        outputFiles.write(response)
        outputFiles.write("\n\n")
