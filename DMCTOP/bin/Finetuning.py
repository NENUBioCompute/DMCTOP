import linecache

class Finetuning():
    def part(self,seq):
        seqLength = len(seq)
        period = []
        i = 0
        count = 0
        while i < seqLength:
            if seq[i] != 'M':
                i = i+1
            else:
                if i == seqLength-1:
                    break
                start = i
                while seq[i+1] == 'M':
                    i = i+1
                    if i == seqLength-1:
                        break
                end = i
                if end-start >= 9:
                    period.append((start,end))
                else:
                    i = i+1
        return period
    
    def replace(self,PartSeq):
        length = len(PartSeq)
        countI = 0
        countM = 0
        countO = 0
        for each in PartSeq:
            if each == 'I':
                countI = countI+1
            elif each == 'M':
                countM = countM+1
            elif each == 'O':
                countO = countO+1
        if countI >= countM and countI >= countO:
            newSeq = ''
            for i in range(length):
                newSeq = newSeq+'I'
            return newSeq
        elif countM >= countI and countM >= countO:
            newSeq = ''
            for i in range(length):
                newSeq = newSeq+'M'
            return newSeq
        elif countO >= countI and countO >= countM:
            newSeq = ''
            for i in range(length):
                newSeq = newSeq+'O'
            return newSeq
                 
    def divide(self,partlist,seq):
        length = len(partlist)
        seqlength = len(seq)
        period = []
        i = 0
        while i < length:
            if i == 0 and i == length-1:
                if partlist[i][0] == 0 and partlitst[i][1] != seqlength-1:
                    period.append((partlist[i][1]+1,seqlength-1))
                elif partlist[i][0] != 0 and partlist[i][1] == seqlength-1:
                    period.append((0,partlist[i][0]-1))
                elif partlist[i][0] != 0 and partlist[i][1] != seqlength-1:
                    period.append((0,partlist[i][0]-1))
                    period.append((partlist[i][1]+1,seqlength-1))
            elif i != 0 and i == length-1:
                if partlist[i][1] == seqlength-1:
                    period.append((partlist[i-1][1]+1,partlist[i][0]-1))
                else:
                    period.append((partlist[i-1][1]+1,partlist[i][0]-1))
                    period.append((partlist[i][1]+1,seqlength-1))
            elif i == 0 and i != length-1:
                if partlist[i][0] != 0:
                    period.append((0,partlist[i][0]-1))
            elif i != 0 and i != length-1:
                period.append((partlist[i-1][1]+1,partlist[i][0]-1))
            i = i+1
        return period
    
    def uniform(self,periodlist,seq):
        for each in periodlist:
            newseq = self.replace(seq[each[0]:each[1]+1])
            seq = seq[0:each[0]]+newseq+seq[each[1]+1:len(seq)]
        return seq
    
    def IOtransform(self,IOlist,seq):
        listLength = len(IOlist)
        for i in range(0,listLength-1):
            standard = int(IOlist[i][0])
            label = seq[standard]
            test = int(IOlist[i+1][0])
            testlabel = seq[test]
            if label == 'I' and testlabel == 'I':
                newseq = ''
                for t in range(IOlist[i+1][0],IOlist[i+1][1]+1):
                    newseq = newseq+'O'
                seq = seq[0:IOlist[i+1][0]]+newseq+seq[IOlist[i+1][1]+1:len(seq)]
            elif label == 'O' and testlabel == 'O':
                newseq = ''
                for t in range(IOlist[i+1][0],IOlist[i+1][1]+1):
                    newseq = newseq+'I'
                seq = seq[0:IOlist[i+1][0]]+newseq+seq[IOlist[i+1][1]+1:len(seq)]
        return seq
    
    def Result(self,seq):
        Mlist = self.part(seq)
        IOlist = self.divide(Mlist,seq)
        newseq = self.uniform(IOlist,seq)
        seq = self.IOtransform(IOlist,newseq)
        return seq

                    
                    
