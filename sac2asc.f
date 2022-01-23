      Program sac2asc
      integer npts1,npts2,i,nptsz
      real dt1,dt2,dtz,Parr,Sarr,t,t1,t2,b,mz
      real y1(100000),y2(100000),yz(100000)
      character*50 fn1,fn2,fnz
      character*1  typ

      open(100,file='result')

      read(*,*)typ
      read(*,*)fnz
      read(*,*)fn1
      read(*,*)fn2

      call RSAC1(fnz,yz,nlen,beg,del,100000,nerr)
      call getnhv('NPTS',nptsz,nerr)
      call getfhv('DELTA',dtz,nerr)

      call RSAC1(fn1,y1,nlen,beg,del,100000,nerr)
      call getnhv('NPTS',npts1,nerr)
      call getfhv('DELTA',dt1,nerr)
      call getfhv('B',b,nerr)
      call getfhv('T1',t1,nerr)
      call getfhv('T2',t2,nerr)
      call getfhv('T3',t3,nerr)
      call getfhv('T4',t4,nerr)

      call RSAC1(fn2,y2,nlen,beg,del,100000,nerr)
      call getnhv('NPTS',npts2,nerr)
      call getfhv('DELTA',dt2,nerr)

      Parr=t1-b
      Sarr=t2-b

      if ((t4 - (-12345)) < 0.00000001)then
         t4 = b
      endif

c     rmean Z-comp.
      mz=sum(yz)/npts1
      do i = 1, npts1
         yz(i)=yz(i)-mz
      enddo

c      Output ascii
      open(100,file='data.asc',status='new')
      write(100,*)Parr,Sarr,typ
      do i = 1, npts1
           t=(i-1)*dt1
           if (t <= t3-b .and. t >= t4-b )then
               write(100,'(f10.5,2X,f10.5,2X,f10.5,2X,f10.5)')
     1             t,yz(i),y1(i),y2(i)
           endif
      enddo
      close(100)      
      stop
      end
