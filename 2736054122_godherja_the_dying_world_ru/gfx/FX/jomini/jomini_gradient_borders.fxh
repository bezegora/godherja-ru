Includes = {
	"jomini/jomini_colormap.fxh"
	"jomini/jomini_colormap_constants.fxh"
}

ConstantBuffer( GradientBorders )
{
	float GB_GradientAlphaInside;
	float GB_GradientAlphaOutside;
	float GB_GradientWidth;
	float GB_GradientColorMul;
	float GB_EdgeWidth;
	float GB_EdgeSmoothness;
	float GB_EdgeAlpha;
	float GB_EdgeColorMul;
	float GB_PreLightingBlend;
	float GB_PostLightingBlend;
}

PixelShader = 
{
	TextureSampler ProvinceColorIndirectionTexture
	{
		Ref = JominiProvinceColorIndirection
		MagFilter = "Point"
		MinFilter = "Point"
		MipFilter = "Point"
		SampleModeU = "Border"
		SampleModeV = "Border"
		Border_Color = { 0 0 0 0 }
	}
	TextureSampler ProvinceColorTexture
	{
		Ref = JominiProvinceColor
		MagFilter = "Point"
		MinFilter = "Point"
		MipFilter = "Point"
		SampleModeU = "Clamp"
		SampleModeV = "Clamp"
	}
	TextureSampler BorderDistanceTexture
	{
		Ref = JominiBorderDistance
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Clamp"
		SampleModeV = "Clamp"
	}

	Code
	[[
		//#define GRADIENT_BORDER_SAMPLES_MEDIUM
		#define GRADIENT_BORDER_SAMPLES_HIGH
		float SampleGradientBorder( in float2 NormalizedCoordinate, in PdxTextureSampler2D DistanceField )
		{
			float Distance = PdxTex2D( DistanceField, NormalizedCoordinate ).r;
			
			#if defined( GRADIENT_BORDER_SAMPLES_MEDIUM ) || defined( GRADIENT_BORDER_SAMPLES_HIGH )
			float2 Offset = vec2(.75f) * InvGradientTextureSize; // (at the time of writing) this equals 3 color map texels
			Distance += PdxTex2D( DistanceField, NormalizedCoordinate + ( Offset * float2( -1,-1 ) ) ).r;
			Distance += PdxTex2D( DistanceField, NormalizedCoordinate + ( Offset * float2(  1,-1 ) ) ).r;
			Distance += PdxTex2D( DistanceField, NormalizedCoordinate + ( Offset * float2( -1, 1 ) ) ).r;
			Distance += PdxTex2D( DistanceField, NormalizedCoordinate + ( Offset * float2(  1, 1 ) ) ).r;
			#endif
			
			#if defined( GRADIENT_BORDER_SAMPLES_HIGH )
			Distance += PdxTex2D( DistanceField, NormalizedCoordinate + ( Offset * float2( -1, 0 ) ) ).r;
			Distance += PdxTex2D( DistanceField, NormalizedCoordinate + ( Offset * float2(  1, 0 ) ) ).r;
			Distance += PdxTex2D( DistanceField, NormalizedCoordinate + ( Offset * float2(  0, 1 ) ) ).r;
			Distance += PdxTex2D( DistanceField, NormalizedCoordinate + ( Offset * float2(  0,-1 ) ) ).r;
			#endif
			
			#if defined( GRADIENT_BORDER_SAMPLES_HIGH )
				Distance /= 9.0f;
			#elif defined( GRADIENT_BORDER_SAMPLES_MEDIUM )
				Distance /= 5.0f;
			#endif
			
			return Distance;
		}
		
		void CalcGradientBorderColorOverlay( 
			in float2 NormalizedCoordinate,
			out float3 ColorOverlay,
			out float PreLightingBlend,
			out float PostLightingBlend,
			in PdxTextureSampler2D IndirectionMap,
			in PdxTextureSampler2D ColorMap,
			in float2 SecondaryColorMapOffset,
			in PdxTextureSampler2D DistanceField )
		{
			float4 PrimaryColor = BilinearColorSample( NormalizedCoordinate, IndirectionMapSize, InvIndirectionMapSize, IndirectionMap, ColorMap );

			// MOD(godherja)

			// color for k_france is { 15 27 187 }
			const float3 DISCARDED_COLOR = float3(0.0, 0.0, 0.0);

			float KeepColorStepValue = step(0.03, distance(PrimaryColor.rgb, DISCARDED_COLOR));

			PrimaryColor = lerp(float4(0.0, 0.0, 0.0, 0.0), PrimaryColor, KeepColorStepValue);
			// END MOD

			float Distance = SampleGradientBorder( NormalizedCoordinate, DistanceField );
			
			float GradientAlpha = lerp(  GB_GradientAlphaInside, GB_GradientAlphaOutside, RemapClamped( Distance, GB_EdgeWidth+GB_GradientWidth, GB_EdgeWidth, 0.0f, 1.0f ) );
			float Edge = smoothstep( GB_EdgeWidth + max(0.0001f,GB_EdgeSmoothness), GB_EdgeWidth, Distance );
			
			float4 Color;
			Color.rgb = lerp( PrimaryColor.rgb * GB_GradientColorMul, PrimaryColor.rgb * GB_EdgeColorMul, Edge );
			Color.a = PrimaryColor.a * max( GradientAlpha * (1.0f - pow( Edge, 2 ) ), GB_EdgeAlpha * Edge );
			
			//#ifdef GRADIENT_BORDER_SECONDARY_COLOR
				float4 SecondaryColor = BilinearColorSampleAtOffset( NormalizedCoordinate, IndirectionMapSize, InvIndirectionMapSize, IndirectionMap, ColorMap, SecondaryColorMapOffset );
				SecondaryColor.a *= smoothstep( GB_EdgeWidth, GB_EdgeWidth + 0.01f, Distance );
				ApplySecondaryColor( Color, SecondaryColor, 0.8, NormalizedCoordinate );				
			//#endif
			
			ColorOverlay = Color.rgb;
			
			PreLightingBlend = GB_PreLightingBlend * Color.a;
			PostLightingBlend = GB_PostLightingBlend * Color.a;
		}
		
		void GetBorderColorAndBlend( float2 NormalizedCoordinate, out float3 BorderColor, out float BorderPreLightingBlend, out float BorderPostLightingBlend )
		{		
			CalcGradientBorderColorOverlay( NormalizedCoordinate, BorderColor, BorderPreLightingBlend, BorderPostLightingBlend, ProvinceColorIndirectionTexture, ProvinceColorTexture, SecondaryProvinceColorsOffset, BorderDistanceTexture );			
		}
	]]
}
