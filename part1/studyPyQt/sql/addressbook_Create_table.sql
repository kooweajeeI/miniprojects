CREATE TABLE addressbook (
  Idx int NOT NULL AUTO_INCREMENT COMMENT 'pk 자동증가',
  FullName varchar(50) NOT NULL COMMENT '이름',
  PhoneNum varchar(20) NOT NULL COMMENT '핸드폰번호',
  Email varchar(120) DEFAULT NULL COMMENT '이메일 (Null 허용)',
  Address varchar(250)  DEFAULT NULL COMMENT '주소 (Null 허용)',
  PRIMARY KEY (Idx)
) COMMENT='주소록 테이블';
