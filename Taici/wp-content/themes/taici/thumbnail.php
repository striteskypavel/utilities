

<!-- Thumbnail from Custom Field, Post first image or default thumbnail 



<div class="thumbnail">
<?php include(TEMPLATEPATH."/thumbnail.php"); ?>
</div>

-->

<div class="thumbnail"><a href="<?php the_permalink() ?>" rel="bookmark">
<?php
$PostContent = $post->post_content;
$ImgSearch = '|<img.*?src=[\'"](.*?)[\'"].*?>|i';
preg_match_all( $ImgSearch, $PostContent, $PostImg );
$ImgNumber = count($PostImg[0]);

    if ( get_post_meta($post->ID, "Thumbnail", true) )
  { ?>
        <img src="<?php echo get_post_meta($post->ID, "Thumbnail", true); ?>" alt="<?php the_title(); ?>" />
<?php }
    elseif ( get_post_meta($post->ID, "thumbnail", true) )
  { ?>
        <img src="<?php echo get_post_meta($post->ID, "thumbnail", true); ?>" alt="<?php the_title(); ?>" />
<?php }
    elseif ( $ImgNumber > 0 )
  {
    for ( $i=0; $i < $ImgNumber ; $i++ )
     {
        echo $PostImg[0][$i];
     };
}
    else
    { ?>
        <img src="<?php bloginfo('stylesheet_directory');?>/images/thumbnail.png" alt="thumbnail"/>
<?php } ?></a></div>
