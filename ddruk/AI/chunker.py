from common_imports import *

class TikTokenUtil:
  def __init__(self,verbose=0):
    self.tokenizer = tiktoken.get_encoding('cl100k_base')
    self.verbose = verbose
  # create the length function

  def concat_maintext(self, vectors):
    res = ""
    token_counts = []
    for v,vec in enumerate(vectors):
      token_counts.append(self.tiktoken_len(vectors[v]['text']))
      res+=vectors[v]['text']
      res+='\n\n'

    if self.verbose:
      print(f"""Min : {min(token_counts)}    Avg: {int(sum(token_counts) / len(token_counts))}   Max: {max(token_counts)}""")
      # set style and color palette for the plot
      sns.set_style("whitegrid")
      sns.set_palette("muted")
      # create histogram
      plt.figure(figsize=(4, 2))
      sns.histplot(token_counts, kde=False, bins=50)
      # customize the plot info
      plt.title("Token Counts Histogram")
      plt.xlabel("Token Count")
      plt.ylabel("Frequency")
      plt.show()
    return res

  def tiktoken_len(self, text):
      tokens = self.tokenizer.encode(
          text,
          disallowed_special=()
      )
      return len(tokens)

  def __call__(self, vectors):
    all_reviews_concat_text = self.concat_maintext(vectors)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20,  # number of tokens overlap between chunks
        length_function=self.tiktoken_len,
        separators=['\n\n', '\n', ' ', '']
    )
    chunks = text_splitter.split_text(all_reviews_concat_text)
    return chunks