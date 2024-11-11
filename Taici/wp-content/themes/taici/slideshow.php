<div id="featured">
<div class="navleft"><a href="#" title="předchozí">&nbsp;</a></div>
<div id="slideshow">

<!-- vložení -->
<?php query_posts('posts_per_page=5&tag=reference'); ?>
<?php if (have_posts()) : ?>
<?php while (have_posts()) : the_post(); ?>

<div>
<div class="edit"><?php edit_post_link('Upravit', '', ''); ?></div>
<a href="<?php bloginfo('url'); ?>/rubrika/reference" class="slide-reference">Ostatní reference &raquo;</a>

<div class="slide"><a href="<?php the_permalink() ?>" title="<?php the_title(); ?>"><?php the_title(); ?></a></div>
<?php the_content(); ?>
<div class="clear space"></div>
</div><!-- / -->

<?php endwhile;?>
<?php else : ?>
<?php endif; ?> 
<?php wp_reset_query(); ?>
<!-- /vložení -->

</div><!-- / slideshow -->

<div class="navright"><a href="#" title="další">&nbsp;</a></div>
</div><!-- /featured -->

<div class="clear"></div>
