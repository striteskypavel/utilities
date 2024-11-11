<?php get_header(); ?>

<?php include(TEMPLATEPATH."/slideshow.php"); ?>

<div id="contentwrap">
<div id="content">


<!-- vložení -->
<?php if (have_posts()) : ?>
<?php while (have_posts()) : the_post(); ?>

<div class="entry">
<div class="edit"><?php edit_post_link('Upravit', '', ''); ?></div>
<h1><?php the_title(); ?></h1>

<div class="post">
<?php the_content(); ?>
<span>(aktualizováno dne: <?php the_time('j. F Y') ?> v rubrice <?php the_category(',') ?>)</span>
</div>

<?php include(TEMPLATEPATH."/social.php"); ?>

</div><!-- / entry -->
<div class="clear space"></div>

<?php endwhile;?>
<?php else : ?>
<?php endif; ?> 
<!-- /vložení -->


</div><!-- /content -->

<?php get_sidebar(); ?>

<div class="clear"></div>

</div><!-- /contentwrap -->

<div class="clear"></div>
	
	
<?php get_footer(); ?>
