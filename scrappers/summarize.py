from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
# import nltk

# # Ensure NLTK tokenizers are available
# nltk.download('punkt_tab')

def summarize_text(text: str, ratio: float = 0.3) -> str:
    """
    Summarize text using Sumy LSA summarizer.

    Parameters:
    - text: The original text to summarize.
    - ratio: Fraction of sentences to keep in the summary (0 < ratio <= 1).

    Returns:
    - A summarized string.
    """
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()

    total_sentences = len(parser.document.sentences)
    if total_sentences == 0:
        return text

    summary_count = max(1, int(total_sentences * ratio))
    summary_sentences = summarizer(parser.document, summary_count)
    return " ".join(str(sentence) for sentence in summary_sentences)
