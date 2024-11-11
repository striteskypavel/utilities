<?php 

// Activate widgets
if ( function_exists('register_sidebar') )
    register_sidebar(array(
        'before_widget' => '<div class="widget">',
        'after_widget' => '<div class="br-h"></div>
		</div>',
        'before_title' => '<h3>',
        'after_title' => '</h3>',
    ));

// Tagcloud
add_action("widgets_init", array('Tag_cloud_modified', 'register'));
class Tag_cloud_modified
{
  function widget($args){
    echo $args['before_widget'];
    echo $args['before_title'] . 'Tag Cloud' . $args['after_title'];
    echo wp_tag_cloud('number=25&format=list&smallest=12&largest=12&unit=px');
    echo $args['after_widget'];
  }

  function register()
  {
    register_sidebar_widget('Tag Cloud', array('Tag_cloud_modified', 'widget'));
    unregister_widget('WP_Widget_Tag_Cloud');
  }
}
// Validate search widget
function valid_search_form ($form) {
    return str_replace('role="search" ', '', $form);
}
add_filter('get_search_form', 'valid_search_form');

// Activate post thumbnails
add_theme_support( 'post-thumbnails' );

// Excerpt hacks	
function new_excerpt_more($post) {
return '&nbsp;&nbsp;<a href="'. get_permalink($post->ID) . '">' . 'more...' . '</a>'; }

add_filter('excerpt_more', 'new_excerpt_more');
function new_excerpt_length($length) { return 40; }
add_filter('excerpt_length', 'new_excerpt_length');

?>