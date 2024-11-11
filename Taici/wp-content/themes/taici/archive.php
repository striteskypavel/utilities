<?php get_header(); ?>

<?php include(TEMPLATEPATH."/slideshow.php"); ?>

<div id="contentwrap">
<div id="content">


		<?php if (have_posts()) : ?>

 	  <?php $post = $posts[0]; // Hack. Set $post so that the_date() works. ?>
 	  
<div class="kategorie"> 
		<h1>
<?php /* Toto je archiv kategorie */ if (is_category()) { ?>
<?php single_cat_title(); ?>
 	  
<?php /* Toto je archiv témat */ } elseif( is_tag() ) { ?>
<?php single_tag_title(); ?>
 	  
<?php /* Toto je archiv denní */ } elseif (is_day()) { ?>
Archiv pro den: <?php the_time('F jS Y'); ?>
 	  
<?php /* Toto je archiv měsíční */ } elseif (is_month()) { ?>
Archiv pro měsíc: <?php the_time('F Y'); ?>
 	  
<?php /* Toto je archiv roční */ } elseif (is_year()) { ?>
Archiv pro rok: <?php the_time('Y'); ?>
 	  <?php } ?>

 	  </h1></div>
 	  
<div class="clear space"></div>
 	  
<?php while (have_posts()) : the_post(); ?>

<div class="entry news">
<div class="edit"><?php edit_post_link('Upravit', '', ''); ?></div>
<h2><a href="<?php the_permalink() ?>" title="<?php the_title(); ?>"><?php the_title(); ?></a></h2>
<div class="post">
<?php the_content(); ?>
<span>(aktualizováno dne <?php the_time('j. F Y') ?> v rubrice <?php the_category(',') ?>)</span>
</div>

<?php include(TEMPLATEPATH."/social.php"); ?>

</div><!-- / entry -->
<div class="clear space"></div>

<?php endwhile;?>
		<div class="postnav">
			<?php wp_pagenavi(); ?>
      <div class="clear"></div>
		</div>
<?php else : ?>
		<h2>Not Found</h2>
		<p>Sorry, but you are looking for something that isn't here.</p>

<?php endif; ?> 
<!-- /vložení -->






</div><!-- /content -->

<?php get_sidebar(); ?>

<div class="clear"></div>

</div><!-- /contentwrap -->

<div class="clear"></div>
	
	
<?php get_footer(); ?>
