<script setup lang="ts">
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

const props = defineProps<{
	label: string;
	content: string;
}>();
</script>

<template>
	<Card class="min-w-32 shadow-none justify-start border-primary bg-primary/10 border-dashed py-6 px-4">
		<CardContent class="p-0">
			<CardHeader class="p-0">
				<CardTitle class="font-semibold">
					{{ props.label }}
				</CardTitle>
			</CardHeader>
			<p class="text-lg">
				{{ props.content }}
			</p>
		</CardContent>
	</Card>
</template>
