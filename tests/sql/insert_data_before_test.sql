-- 测试分类和标签
TRUNCATE TABLE `wp_terms`;
INSERT INTO `wp_terms` (`term_id`, `name`, `slug`, `term_group`) VALUES ('1', '未分类', 'uncategorized', '0');
INSERT INTO `wp_terms` (`term_id`, `name`, `slug`, `term_group`) VALUES ('2', '测试分类', 'test_favorite', '0');
INSERT INTO `wp_terms` (`term_id`, `name`, `slug`, `term_group`) VALUES ('3', '测试标签', 'test_tag', '0');

-- 测试分类和标签的元数据
TRUNCATE TABLE `wp_termmeta`;
INSERT INTO `wp_termmeta` (`meta_id`, `term_id`, `meta_key`, `meta_value`) VALUES ('1', '2', '_term_order', '99');
INSERT INTO `wp_termmeta` (`meta_id`, `term_id`, `meta_key`, `meta_value`) VALUES ('2', '2', 'seo_title', 'SEO 标题');
INSERT INTO `wp_termmeta` (`meta_id`, `term_id`, `meta_key`, `meta_value`) VALUES ('3', '2', 'seo_metakey', 'SEO 关键词一、关键词2');
INSERT INTO `wp_termmeta` (`meta_id`, `term_id`, `meta_key`, `meta_value`) VALUES ('4', '2', 'seo_desc', 'SEO 描述');
INSERT INTO `wp_termmeta` (`meta_id`, `term_id`, `meta_key`, `meta_value`) VALUES ('5', '2', 'card_mode', 'null');
INSERT INTO `wp_termmeta` (`meta_id`, `term_id`, `meta_key`, `meta_value`) VALUES ('6', '2', 'columns_type', 'global');
INSERT INTO `wp_termmeta` (`meta_id`, `term_id`, `meta_key`, `meta_value`) VALUES ('7', '2', 'columns', 'a:5:{s:2:\"sm\";s:1:\"2\";s:2:\"md\";s:1:\"2\";s:2:\"lg\";s:1:\"3\";s:2:\"xl\";s:1:\"5\";s:3:\"xxl\";s:1:\"6\";}');
INSERT INTO `wp_termmeta` (`meta_id`, `term_id`, `meta_key`, `meta_value`) VALUES ('8', '3', 'sitetag_meta', 'a:3:{s:9:\"seo_title\";s:19:\"SEO 自定义标题\";s:11:\"seo_metakey\";s:25:\"关键词一、关键词2\";s:8:\"seo_desc\";s:15:\"自定义描述\";}');

-- 分类和标签的关系
TRUNCATE TABLE `wp_term_taxonomy`;
INSERT INTO `wp_term_taxonomy` (`term_taxonomy_id`, `term_id`, `taxonomy`, `description`, `parent`, `count`) VALUES ('1', '1', 'category', '', '0', '0');
INSERT INTO `wp_term_taxonomy` (`term_taxonomy_id`, `term_id`, `taxonomy`, `description`, `parent`, `count`) VALUES ('2', '2', 'favorites', '测试分类的描述', '0', '0');
INSERT INTO `wp_term_taxonomy` (`term_taxonomy_id`, `term_id`, `taxonomy`, `description`, `parent`, `count`) VALUES ('3', '3', 'sitetag', '测试描述\r\n另起一行。', '0', '0');