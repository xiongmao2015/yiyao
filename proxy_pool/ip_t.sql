CREATE TABLE `ip_t` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `ip` varchar(16) NOT NULL COMMENT 'ip地址',
  `port` varchar(8) NOT NULL COMMENT '端口',
  `country` varchar(64) NOT NULL COMMENT '国家',
  `anonymous` varchar(16) NOT NULL COMMENT '匿名',
  `http_type` varchar(16) NOT NULL COMMENT 'http类型',
  `from_site` varchar(32) NOT NULL COMMENT '来源网站',
  `status` varchar(2) DEFAULT NULL COMMENT '状态',
  `crawl_time` datetime NOT NULL COMMENT '抓取时间',
  `ip_md5` varchar(32) NOT NULL UNIQUE COMMENT 'ip_md5',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;