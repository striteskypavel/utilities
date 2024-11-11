<?php get_header(); ?>

<?php include(TEMPLATEPATH."/slideshow.php"); ?>

<div id="contentwrap">
<div id="content">

<h1>Search results:</h1>
<div class="br-h"></div>
<?php if (have_posts()) : ?>
<?php while (have_posts()) : the_post(); ?>

<div class="entry">

<h3><a href="<?php the_permalink() ?>"><?php the_title(); ?></a></h3>

<span><?php the_time('F jS, Y') ?> | <?php the_category(',') ?> | <?php comments_popup_link('No Comments &#187;', '1 Comment &#187;', '% Comments &#187;', 'comments-link', ''); ?></span>

<?php the_excerpt(); ?>
<?php the_tags('<div class="tags"><strong>Tags:</strong> ', ', ', '<br /></div>'); ?>

<div class="br-h"></div>
</div><!-- /entry -->
<?php endwhile;?>
		<div class="postnav">
			<div class="alignleft"><?php next_posts_link('&laquo; Older Entries') ?></div>
			<div class="alignright"><?php previous_posts_link('Newer Entries &raquo;') ?></div>
		</div>
<?php else : ?>
		<h3>No posts found. Try a different search?</h3>
		<?php get_search_form(); ?>

<?php endif; ?> 


</div><!-- /content -->

<?php get_sidebar(); ?>

<div class="clear"></div>

</div><!-- /contentwrap -->

<div class="clear"></div>
	
	
<?php get_footer(); ?>
