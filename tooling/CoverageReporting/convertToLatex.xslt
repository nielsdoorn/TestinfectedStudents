<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="text" indent="no"/>


     <xsl:template match="coverage">
        <xsl:copy>
            <xsl:apply-templates/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="project">
        <xsl:copy>
            <xsl:apply-templates/>
        </xsl:copy>
    </xsl:template>

     <xsl:template match="coverage/project/metrics">
       <xsl:value-of select="@coveredelements"/> &amp; <xsl:value-of select="@complexity"/> \\
    </xsl:template>

    <!--
 <metrics 
 coveredelements="38" 
 complexity="17" 
 loc="164" 
 methods="14" 
 classes="3" 
 statements="31" 
 packages="1" 
 coveredconditionals="5" 
 coveredmethods="10" 
 elements="51" 
 ncloc="87" 
 files="3" 
 conditionals="6" 
 coveredstatements="23"/>


      {Project id}            & {Branch} & {Statement} & {Method} & {Total}  & {LOC}        & {NCLOC} & {Files} & {Methods} & {Classes} \\ 
      
         
          -->
</xsl:stylesheet>
