class Summarizer:
    def summarize(self, text: str) -> str:
        raise NotImplementedError


if __name__ == '__main__':
    text = '''
As a child, Gandhi was described by his sister Raliat as "restless as mercury, either playing or roaming about. One of his favourite pastimes was twisting dogs' ears."[16] The Indian classics, especially the stories of Shravana and king Harishchandra, had a great impact on Gandhi in his childhood. In his autobiography, he states that they left an indelible impression on his mind. He writes: "It haunted me and I must have acted Harishchandra to myself times without number." Gandhi's early self-identification with truth and love as supreme values is traceable to these epic characters.[17][18]

The family's religious background was eclectic. Mohandas was born into a Gujarati Hindu Modh Bania family.[19][20] Gandhi's father Karamchand was Hindu and his mother Putlibai was from a Pranami Vaishnava Hindu family.[21][22] Gandhi's father was of Modh Baniya caste in the varna of Vaishya.[23] His mother came from the medieval Krishna bhakti-based Pranami tradition, whose religious texts include the Bhagavad Gita, the Bhagavata Purana, and a collection of 14 texts with teachings that the tradition believes to include the essence of the Vedas, the Quran and the Bible.[22][24] Gandhi was deeply influenced by his mother, an extremely pious lady who "would not think of taking her meals without her daily prayers... she would take the hardest vows and keep them without flinching. To keep two or three consecutive fasts was nothing to her."[25]


Gandhi (right) with his eldest brother Laxmidas in 1886[26]
At age 9, Gandhi entered the local school in Rajkot, near his home. There, he studied the rudiments of arithmetic, history, the Gujarati language and geography.[15] At the age of 11, he joined the High School in Rajkot, Alfred High School.[27] He was an average student, won some prizes, but was a shy and tongue tied student, with no interest in games; his only companions were books and school lessons.[28]
    '''
    print(Summarizer().summarize(text))
