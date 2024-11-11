<?php get_header(); ?>

<?php include(TEMPLATEPATH."/slideshow.php"); ?>

<div id="contentwrap">
<div id="content">

		<h1>Tato stránka nebyla nalezena, <br />na webu aktuálně naleznete tyto stránky:</h1>
		
	<?php query_posts('posts_per_page=9999'); ?>
  <?php if (have_posts()) : while (have_posts()) : the_post(); ?> 
  <a href="<?php the_permalink() ?>"><?php the_permalink() ?></a><br />
  <?php endwhile; ?>
  <?php else : ?>
  <?php endif; ?>
  <?php wp_reset_query();?>

</div><!-- /content -->

<?php get_sidebar(); ?>

<div class="clear"></div>

</div><!-- /contentwrap -->

<div class="clear"></div>
	
	
<?php get_footer(); ?>
