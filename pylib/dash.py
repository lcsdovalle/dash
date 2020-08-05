class dashParam():
    def __init__(self):
        self.totalProfessores = 0
        self.totalAlunos = 0
        self.totalOutros = 0
        self.totalJaLogaram = 0
        self.totalNuncaLogaram = 0
        self.totalEscolas = 0
        self.totalTeachersLogaram = 0
        self.totalStudentsLogaram = 0
        self.totalOthersLogaram = 0
        self.totalSchoolsLogaram = 0
        self.totalTurmas = 0
        self.totalUsers = 0
        self.totalAlunosMedio = 0
        self.totalAlunosMedioJaLogaram = 0
        self.totalAlunosFundamentalI = 0
        self.totalAlunosFundamentalII = 0
        self.totalAlunosFundamentalIJalogaram = 0
        self.totalAlunosFundamentalIIJalogaram = 0
    def setTotalAlunosFundamentalIJalogaram(self):
        self.totalAlunosFundamentalIJalogaram += 1
    def getTotalAlunosFundamentalIJalogaram(self):
        return self.totalAlunosFundamentalIJalogaram

    def setTotalAlunosFundamentalIIJalogaram(self):
        self.totalAlunosFundamentalIIJalogaram += 1
    def getTotalAlunosFundamentalIIJalogaram(self):
        return self.totalAlunosFundamentalIIJalogaram

    def setTotalAlunosFundamentalI(self):
        self.totalAlunosFundamentalI += 1
    def getTotalAlunosFundamentalI(self):
        return self.totalAlunosFundamentalI
        
    def setTotalAlunosFundamentalII(self):
        self.totalAlunosFundamentalII += 1
    def getTotalAlunosFundamentalII(self):
        return self.totalAlunosFundamentalII
        
    def setTotalProfessores(self):
        self.totalProfessores +=1 
    def setTotalAlunos(self):
        self.totalAlunos +=1 
    def setTotalOutros(self):
        self.totalOutros +=1 
    def setTotalJaLogaram(self):
        self.totalJaLogaram +=1 
    def setTotalNuncaLogaram(self):
        self.totalNuncaLogaram +=1 
    def setTotalEscolas(self):
        self.totalEscolas +=1 
    def setTotalTeachersLogaram(self):
        self.totalTeachersLogaram +=1   
    def setTotalStudentsLogaram(self):
        self.totalStudentsLogaram +=1  
    def setTotalOthersLogaram(self):
        self.totalOthersLogaram +=1  
    def setTotalSchoolsLogaram(self):
        self.totalSchoolsLogaram +=1  
    def setTotalTurmas(self,value):
        self.totalTurmas += int(value)
    def setTotalUsers(self,value):
        self.totalUsers += value
    def setTotalAlunosMedio(self):
        self.totalAlunosMedio += 1
    def setTotalAlunosMedioJaLogaram(self):
        self.totalAlunosMedioJaLogaram += 1
    def getTotalProfessores(self):
        return self.totalProfessores
    def getTotalAlunos(self):
        return self.totalAlunos
    def getTotalOutros(self):
        return self.totalOutros
    def getTotalJaLogaram(self):
        return self.totalJaLogaram
    def getTotalNuncaLogaram(self):
        return self.totalNuncaLogaram
    def getTotalEscolas(self):
        return self.totalEscolas
    def getTotalTeachersLogaram(self):
        return self.totalTeachersLogaram
    def getTotalStudentsLogaram(self):
        return self.totalStudentsLogaram  
    def getTotalOthersLogaram(self):
        return self.totalOthersLogaram
    def getTotalSchoolsLogaram(self):
        return self.totalSchoolsLogaram  
    def getTotalTurmas(self):
        return self.totalTurmas 
    def getTotalUsers(self):
        return self.totalUsers
    def getTotalAlunosMedio(self):
        return self.totalAlunosMedio
    def getTotalAlunosMedioJaLogaram(self):
        return self.totalAlunosMedioJaLogaram