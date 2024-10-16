-- 清空数据表
TRUNCATE TABLE `wp_terms`;
TRUNCATE TABLE `wp_termmeta`;
TRUNCATE TABLE `wp_term_taxonomy`;
TRUNCATE TABLE `wp_term_relationships`;
TRUNCATE TABLE `wp_posts`;
TRUNCATE TABLE `wp_postmeta`;

-- 测试分类和标签
INSERT INTO `wp_terms` (`term_id`, `name`, `slug`, `term_group`) VALUES ('1', '未分类', 'uncategorized', '0');
INSERT INTO `wp_terms` (`term_id`, `name`, `slug`, `term_group`) VALUES ('2', '测试分类', 'test_favorite', '0');
INSERT INTO `wp_terms` (`term_id`, `name`, `slug`, `term_group`) VALUES ('3', '测试标签', 'test_tag', '0');

-- 测试分类和标签的元数据
INSERT INTO `wp_termmeta` (`meta_id`, `term_id`, `meta_key`, `meta_value`) VALUES ('1', '2', '_term_order', '99');
INSERT INTO `wp_termmeta` (`meta_id`, `term_id`, `meta_key`, `meta_value`) VALUES ('2', '2', 'seo_title', 'SEO 标题');
INSERT INTO `wp_termmeta` (`meta_id`, `term_id`, `meta_key`, `meta_value`) VALUES ('3', '2', 'seo_metakey', 'SEO 关键词一、关键词2');
INSERT INTO `wp_termmeta` (`meta_id`, `term_id`, `meta_key`, `meta_value`) VALUES ('4', '2', 'seo_desc', 'SEO 描述');
INSERT INTO `wp_termmeta` (`meta_id`, `term_id`, `meta_key`, `meta_value`) VALUES ('5', '2', 'card_mode', 'null');
INSERT INTO `wp_termmeta` (`meta_id`, `term_id`, `meta_key`, `meta_value`) VALUES ('6', '2', 'columns_type', 'global');
INSERT INTO `wp_termmeta` (`meta_id`, `term_id`, `meta_key`, `meta_value`) VALUES ('7', '2', 'columns', 'a:5:{s:2:\"sm\";s:1:\"2\";s:2:\"md\";s:1:\"2\";s:2:\"lg\";s:1:\"3\";s:2:\"xl\";s:1:\"5\";s:3:\"xxl\";s:1:\"6\";}');
INSERT INTO `wp_termmeta` (`meta_id`, `term_id`, `meta_key`, `meta_value`) VALUES ('8', '3', 'sitetag_meta', 'a:3:{s:9:\"seo_title\";s:19:\"SEO 自定义标题\";s:11:\"seo_metakey\";s:25:\"关键词一、关键词2\";s:8:\"seo_desc\";s:15:\"自定义描述\";}');

-- 分类和标签的关系
INSERT INTO `wp_term_taxonomy` (`term_taxonomy_id`, `term_id`, `taxonomy`, `description`, `parent`, `count`) VALUES ('1', '1', 'category', '', '0', '0');
INSERT INTO `wp_term_taxonomy` (`term_taxonomy_id`, `term_id`, `taxonomy`, `description`, `parent`, `count`) VALUES ('2', '2', 'favorites', '测试分类的描述', '0', '0');
INSERT INTO `wp_term_taxonomy` (`term_taxonomy_id`, `term_id`, `taxonomy`, `description`, `parent`, `count`) VALUES ('3', '3', 'sitetag', '测试描述\r\n另起一行。', '0', '0');

-- 测试网址
INSERT INTO `wp_posts` (
    `ID`,
    `post_author`,
    `post_date`,
    `post_date_gmt`,
    `post_content`,
    `post_title`,
    `post_excerpt`,
    `post_status`,
    `comment_status`,
    `ping_status`,
    `post_password`,
    `post_name`,
    `to_ping`,
    `pinged`,
    `post_modified`,
    `post_modified_gmt`,
    `post_content_filtered`,
    `post_parent`,
    `guid`,
    `menu_order`,
    `post_type`,
    `post_mime_type`,
    `comment_count`
) VALUES (
    '11',
    '1',
    '2024-10-13 20:17:23',
    '2024-10-13 12:17:23',
    '由 Rabbir 编写的脚本。\n仓库地址为：<a href=\"https://github.com/senjianlu/sync-onenav-from-excel\">senjianlu/sync-onenav-from-excel</a>',
    '从 Excel 中同步来的链接',
    '',
    'publish',
    'closed',
    'closed',
    '',
    '%E4%BB%8E%20Excel%20%E4%B8%AD%E5%90%8C%E6%AD%A5%E6%9D%A5%E7%9A%84%E9%93%BE%E6%8E%A5',
    '',
    '',
    '2024-10-13 20:17:23',
    '2024-10-13 12:17:23',
    '',
    '0',
    'https://steam.cash/sites/11.html',
    0,
    'sites',
    '',
    '0'
);

INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('297', '11', '_sync_site_id', '99');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('298', '11', '_views', '0');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('299', '11', '_down_count', '0');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('300', '11', '_like_count', '0');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('301', '11', '_user_purview_level', 'all');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('302', '11', '_edit_last', '1');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('303', '11', '_edit_lock', '1728821844:1');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('304', '11', '_seo_title', '');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('305', '11', '_seo_metakey', '');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('306', '11', '_seo_desc', '');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('307', '11', 'sidebar_layout', 'default');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('308', '11', '_sites_type', 'sites');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('309', '11', '_goto', '0');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('310', '11', '_wechat_id', '');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('311', '11', '_is_min_app', '');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('312', '11', '_down_version', '');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('313', '11', '_down_size', '');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('314', '11', '_down_url_list', '');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('315', '11', '_dec_password', '');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('316', '11', '_app_platform', '');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('317', '11', '_down_preview', '');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('318', '11', '_down_formal', '');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('319', '11', '_screenshot', '');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('320', '11', 'buy_option', 'a:7:{s:8:\"\"buy_type\"\";s:4:\"\"view\"\";s:5:\"\"limit\"\";s:3:\"\"all\"\";s:8:\"\"pay_type\"\";s:5:\"\"money\"\";s:10:\"\"price_type\"\";s:6:\"\"single\"\";s:9:\"\"pay_title\"\";s:0:\"\"\"\";s:9:\"\"pay_price\"\";s:1:\"\"0\"\";s:5:\"\"price\"\";s:1:\"\"0\"\";}');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('321', '11', '_sites_link', 'https://github.com/senjianlu/sync-onenav-from-excel');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('322', '11', '_spare_sites_link', 'a:2:{i:0;a:3:{s:10:"spare_name";s:6:"百度";s:9:"spare_url";s:17:"https://baidu.com";s:10:"spare_note";s:15:"百度备注。";}i:1;a:3:{s:10:"spare_name";s:6:"谷歌";s:9:"spare_url";s:18:"https://google.com";s:10:"spare_note";s:6:"谷歌";}}');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('323', '11', '_sites_sescribe', '将 Excel 中的网址同步到 OneNav 一为导航中。\n详细参考 GitHub 仓库的 README.md。');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('324', '11', '_sites_language', 'zh,en');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('325', '11', '_sites_country', '中国');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('326', '11', '_sites_order', '0');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('327', '11', '_thumbnail', 'https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('328', '11', '_sites_preview', 'https://kinsta.com/wp-content/uploads/2018/04/what-is-github-1-1.png');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`) VALUES ('329', '11', '_wechat_qr');
INSERT INTO `wp_postmeta` (`meta_id`, `post_id`, `meta_key`, `meta_value`) VALUES ('330', '11', 'views', '6');

INSERT INTO `wp_term_relationships` (`object_id`, `term_taxonomy_id`, `term_order`) VALUES ('11', '2', 0);

UPDATE `wp_term_taxonomy` SET `count` = (SELECT COUNT(*) FROM `wp_term_relationships` WHERE `wp_term_relationships`.`term_taxonomy_id` = `wp_term_taxonomy`.`term_taxonomy_id`);