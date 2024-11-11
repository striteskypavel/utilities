<?php get_header(); ?>

<?php include(TEMPLATEPATH."/slideshow.php"); ?>

<div id="contentwrap">
<div id="content">


<!-- vložení info pro zájemce -->
<?php query_posts('page_id=52'); ?>
<?php if (have_posts()) : ?>
<?php while (have_posts()) : the_post(); ?>

<div class="entry">
<div class="edit"><?php edit_post_link('Upravit', '', ''); ?></div>
<h2><a href="<?php the_permalink() ?>" title="<?php the_title(); ?>"><?php the_title(); ?></a></h2>
<div class="post">
<?php the_content(); ?>
</div>

<?php include(TEMPLATEPATH."/social.php"); ?>

</div><!-- / entry -->
<div class="clear space"></div>

<?php endwhile;?>
<?php else : ?>
<?php endif; ?> 
<?php wp_reset_query(); ?>
<!-- /vložení -->


<h2>Aktuální info:</h2>

<!-- vložení -->
<?php query_posts('posts_per_page=3&cat=1'); ?>
<?php if (have_posts()) : ?>
<?php while (have_posts()) : the_post(); ?>

<div class="entry news">
<div class="edit"><?php edit_post_link('Upravit', '', ''); ?></div>
<h2><a href="<?php the_permalink() ?>" title="<?php the_title(); ?>"><?php the_title(); ?></a></h2>
<div class="post">
<?php the_content(); ?>
</div>

<?php include(TEMPLATEPATH."/social.php"); ?>

</div><!-- / entry -->
<div class="clear space"></div>

<?php endwhile;?>
		<div class="postnav">
			<div class="alignright"><a href="<?php bloginfo('url'); ?>/rubrika/novinky" title="Novinky">Všechny novinky &#187;</a></div>
      <div class="clear"></div>
		</div>
<?php else : ?>
<?php endif; ?> 
<?php wp_reset_query(); ?>
<!-- /vložení -->






</div><!-- /content -->

<?php get_sidebar(); ?>

<div class="clear"></div>

</div><!-- /contentwrap -->

<div class="clear"></div>
	
	
<?php get_footer(); ?>
