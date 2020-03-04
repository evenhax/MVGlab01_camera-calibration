import numpy as np
from numpy import linalg as LA

class SingleCamera:

    def __init__ (self,world_coor,pixel_coor,n):

        self.__world_coor=world_coor
        self.__pixel_coor=pixel_coor
        self.__point_num=n

        self.__P=np.empty([self.__point_num,12], dtype = float)
        self.__roM=np.empty([3,4],dtype=float)
        self.__A=np.empty([3,3],dtype = float)
        self.__b = np.empty([3, 1], dtype=float)
        self.__K=np.empty([3,3],dtype=float)
        self.__R=np.empty([3,3],dtype=float)
        self.__t=np.empty([3,1],dtype=float)

    def returnAb(self):
        return self.__A,self.__b

    def returnKRT(self):
        return self.__K,self.__R,self.__t

    def returnM(self):
        return self.__roM

    def myReadFile(filePath):
        pass

    def changeHomo(no_homo):
        pass

    # to compose P in right form
    def composeP(self):
        i=0
        P=np.empty([self.__point_num,12], dtype = float)
        print(P.shape)
        while i<self.__point_num:
            c=i//2
            p1 = self.__world_coor[c]
            p2 = np.array([0,0,0,0])
            if i%2==0:
                p3=-p1*self.__pixel_coor[c][0]
                print(p3)
                P[i]=np.hstack((p1,p2,p3))

            elif i%2==1:
                p3=-p1*self.__pixel_coor[c][1]
                print(p3)
                P[i]=np.hstack((p2,p1,p3))
            M = P[i]
            print(M)
            i=i+1
        print(P)
        self.__P=P

    # svd to P，return A,b
    def svdP(self):
        U, sigma, VT = LA.svd(self.__P)
        print(VT.shape)
        V=np.transpose(VT)
        preM=V[:,-1]
        roM=preM.reshape(3,4)
        print(roM)
        A=roM[0:3,0:3].copy()
        print(A)
        b=roM[0:3,3:4].copy()
        print(b)
        self.__roM=roM
        self.__A=A
        self.__b=b


    def workInAndOut(self):
        # compute ro
        a3T=self.__A[2]
        print(a3T)
        under=LA.norm(a3T)
        print(under)
        ro01=1/under

        #comput cx and cy
        print(ro01)
        a1T=self.__A[0]
        a2T=self.__A[1]
        cx=ro01*ro01*(np.dot(a1T,a3T))
        cy=ro01*ro01*(np.dot(a2T,a3T))
        print(cx,cy)

        #compute theta
        a_cross13=np.cross(a1T,a3T)
        a_cross23=np.cross(a2T,a3T)
        print(a_cross13,a_cross23)

        theta=np.arccos((-1)*np.dot(a_cross13,a_cross23)/(LA.norm(a_cross13)*LA.norm(a_cross23)))
        print(theta)

        #compute alpha and beta
        alpha=ro01*ro01*LA.norm(a_cross13)*np.sin(theta)
        beta=ro01*ro01*LA.norm(a_cross23)*np.sin(theta)

        print(alpha,beta)

        #compute K
        K=np.array([alpha,-alpha*(1/np.tan(theta)),cx,0,beta/(np.sin(theta)),cy,0,0,1])
        K=K.reshape(3,3)
        print(K)
        self.__K=K

        #compute R
        r1=a_cross23/LA.norm(a_cross23)
        r301=ro01*a3T
        r2=np.cross(r301,r1)
        print(r1,r2,r301)
        R=([r1,r2,r301])
        print(R)
        self.__R=R

        #compute T
        T=ro01*np.dot(LA.inv(K),self.__b)
        print(T)
        self.__t=T



