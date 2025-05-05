<script lang="ts" setup>
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import {
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuItem,
	DropdownMenuLabel,
	DropdownMenuSeparator,
	DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { getUploadedFileUrl } from '@/services/api';
import { useGlobalStore } from '@/store';

const gs = useGlobalStore();
const self = gs.user.data;
</script>

<template>
	<DropdownMenu>
		<DropdownMenuTrigger as-child>
			<Avatar>
				<AvatarImage :src="getUploadedFileUrl(self?.photo) ?? ''" :alt="`${self?.name} Avatar`" />
				<AvatarFallback>{{ self?.name?.[0] }}</AvatarFallback>
			</Avatar>
		</DropdownMenuTrigger>
		<DropdownMenuContent>
			<DropdownMenuLabel>{{ self?.name }}</DropdownMenuLabel>
			<DropdownMenuSeparator />
			<DropdownMenuItem as-child>
				<router-link to="/profiles">
					My Profiles
				</router-link>
			</DropdownMenuItem>
			<DropdownMenuSeparator />
			<DropdownMenuItem variant="destructive" onclick="">
				<router-link to="/logout">
					Logout
				</router-link>
			</DropdownMenuItem>
		</DropdownMenuContent>
	</DropdownMenu>
</template>
